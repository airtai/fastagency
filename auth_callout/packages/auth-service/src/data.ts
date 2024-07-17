import { AuthToken, PrismaClient } from "@prisma/client";


export type Auth = {
  user: string;
  password: string;
  chat_uuid: string;
}

const prisma = new PrismaClient();

// const wasp_prisma = new PrismaClient({ datasources: { db: { url: process.env.DATABASE_URL } } })


export async function fetchAuthToken(deployment_uuid: string) {
  try {
    const authTokens: AuthToken[] = await prisma.$queryRaw`SELECT * FROM "AuthToken" WHERE "deployment_uuid" = ${deployment_uuid}::uuid and expires_at > NOW()`;
    return authTokens.length > 0 ? authTokens : null; // Return the authTokens if found, else return null
  } catch (error) {
    console.error('Error fetching AuthToken by deployment_uuid:', error);
    return null; // Return null on error
  }
}

export async function verifyAuthTokens(auth_pass: string, authTokens: AuthToken[]) {
  for (const authToken of authTokens) {
    // check if password is correct
    if (await verifyAuthToken(auth_pass, authToken.auth_token)) {
      return authToken;
    }

  }
  return false;
}

export async function verifyAuthToken(token: string, storedHash: string): Promise<boolean> {
  const parts: Array<string> = storedHash.split(':');
  if (parts.length !== 2) {
    return false;
  }

  // Split the stored hash into salt and hash
  const [salt, hashValue] = parts;
  // Check if salt and hashValue are defined
  if (!salt || !hashValue) {
    return false;
  }

  // Convert salt back to Uint8Array
  const saltBytes = new Uint8Array(salt.match(/.{1,2}/g)!.map(byte => parseInt(byte, 16)));

  // Combine salt and token
  const encoder = new TextEncoder();
  const tokenBytes = encoder.encode(token);
  const saltedToken = new Uint8Array(saltBytes.length + tokenBytes.length);
  saltedToken.set(saltBytes);
  saltedToken.set(tokenBytes, saltBytes.length);

  // Hash the salted token
  const computedHash = crypto.subtle.digest('SHA-256', saltedToken)
    .then(hash => Array.from(new Uint8Array(hash))
      .map(b => b.toString(16).padStart(2, '0'))
      .join('')
    );

  // Compare the computed hash with the stored hash
  return computedHash.then(hash => hash === hashValue);
}
