import * as Nats from "nats";
import * as Jwt from "nats-jwt";
import * as Nkeys from "nkeys.js";
import { Auth, fetchAuthToken, verifyAuthTokens } from "./data";
import { AuthorizationRequestClaims } from "./types";

run();

async function run() {
  let natsUrl: string | undefined;
  natsUrl = process.env.NATS_URL;
  if (!natsUrl) {
    const domain = process.env.DOMAIN;
    natsUrl = `tls://${domain}:4222`;
  }
  const natsUser = "auth";
  const natsPass = process.env.AUTH_NATS_PASSWORD;
  const issuerSeed = process.env.NATS_PRIV_NKEY;
  console.log(`NATS URL: ${natsUrl}`);

  var enc = new TextEncoder();
  var dec = new TextDecoder();

  // Parse the issuer account signing key.
  const issuerKeyPair = Nkeys.fromSeed(enc.encode(issuerSeed));

  // Open the NATS connection passing the auth account creds file.
  const nc = await Nats.connect({ servers: natsUrl, user: natsUser, pass: natsPass });

  // Start subscription
  const sub = nc.subscribe("$SYS.REQ.USER.AUTH");
  console.log(`listening for ${sub.getSubject()} requests...`);
  for await (const msg of sub) {
    console.log("Auth service got message");
    // console.log(msg)
    await msgHandler(msg, enc, dec, issuerKeyPair);
  }
}

async function msgHandler(req: Nats.Msg, enc: TextEncoder, dec: TextDecoder, issuerKeyPair: Nkeys.KeyPair) {
  // Helper function to construct an authorization response.
  const respondMsg = async (req: Nats.Msg, userNkey: string, serverId: string, userJwt: string, errMsg: string) => {
    let token: string;
    try {
      token = await Jwt.encodeAuthorizationResponse(userNkey, serverId, issuerKeyPair, { jwt: userJwt, error: errMsg }, {});
    } catch (err) {
      console.log("error encoding response JWT: %s", err);
      req.respond(undefined);
      return;
    }
    let data = enc.encode(token);
    req.respond(data);
  };

  // Check for Xkey header and decrypt
  let token: Uint8Array = req.data;

  // Decode the authorization request claims.
  let rc: AuthorizationRequestClaims;
  try {
    Jwt.encodeAuthorizationResponse;
    rc = Jwt.decode<AuthorizationRequestClaims>(dec.decode(token)) as AuthorizationRequestClaims;
  } catch (e) {
    return respondMsg(req, "", "", "", (e as Error).message);
  }

  // Used for creating the auth response.
  const userNkey = rc.nats.user_nkey;
  const serverId = rc.nats.server_id.id;

  const auth = rc.nats.connect_opts.auth_token;
  if (!auth) {
    return respondMsg(req, userNkey, serverId, "", "auth token not provided");
  }
  let parsedAuth: Auth;
  try {
    parsedAuth = JSON.parse(auth);
  } catch (e) {
    return respondMsg(req, "", "", "", (e as Error).message);
  }

  const auth_user = parsedAuth.user;
  const auth_pass = parsedAuth.password;
  const chat_uuid = parsedAuth.chat_uuid;

  // auth_user value is deployment_uuid, check authToken is not null
  const authTokens = await fetchAuthToken(auth_user);
  if (!authTokens) {
    return respondMsg(req, userNkey, serverId, "", "user " + auth_user + " not found");
  }

  const authToken = await verifyAuthTokens(auth_pass, authTokens);
  if (!authToken) {
    return respondMsg(req, userNkey, serverId, "", "invalid credentials");
  }

  const grantedRooms = [
    "chat.server.initiate_chat",
    `chat.client.messages.${authToken.user_uuid}.${authToken.deployment_uuid}.${chat_uuid}`,
    `chat.server.messages.${authToken.user_uuid}.${authToken.deployment_uuid}.${chat_uuid}`,
    "_INBOX.>",
    "$JS.API.STREAM.NAMES",
    // `$JS.API.STREAM.NAMES.FastAgency`,
    "$JS.API.CONSUMER.INFO.FastAgency.*",
    "$JS.API.CONSUMER.CREATE.FastAgency",
    "$JS.API.CONSUMER.DURABLE.CREATE.FastAgency.*",
  ];
  console.log(`Auth service user ${auth_user} granted permission to subjects: ${JSON.stringify(grantedRooms)}`);

  // User part of the JWT token to issue
  // Add "public" because if the allowed array is empty then all is allowed
  const user: Partial<Jwt.User> = { pub: { allow: [...grantedRooms], deny: [] }, sub: { allow: [...grantedRooms], deny: [] } };
  console.log(`Auth service permission: ${JSON.stringify(user)}`);
  // Prepare a user JWT.
  let ejwt: string;
  try {
    ejwt = await Jwt.encodeUser(rc.nats.connect_opts.user!, rc.nats.user_nkey, issuerKeyPair, user, { aud: "AUTH" });
  } catch (e) {
    console.log("error signing user JWT: %s", e);
    return respondMsg(req, userNkey, serverId, "", "error signing user JWT");
  }

  return respondMsg(req, userNkey, serverId, ejwt, "");
}
