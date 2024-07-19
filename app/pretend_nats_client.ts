// import { connect, consumerOpts, JSONCodec } from 'nats';
// import { v4 as uuidv4 } from 'uuid';

// const NATS_URL = process.env['NATS_URL'];
// console.log(`NATS_URL=${NATS_URL}`);

// async function generateClientId(): Promise<string> {
//   return uuidv4();
// }

// async function main() {
//   try {
//     if (!NATS_URL) {
//       throw new Error('NATS_URL is not defined');
//     }
//     const nc = await connect({ servers: NATS_URL });
//     console.log(`connected to ${nc.getServer()}`);

//     const js = nc.jetstream();
//     const jc = JSONCodec();
//     const clientId = await generateClientId();

//     const registerSubject = `register.${clientId}`;
//     const pingSubject = `ping.${clientId}`;
//     const pongSubject = `pong.${clientId}`;

//     // Subscribe to messages
//     const opts = consumerOpts();
//     opts.orderedConsumer();
//     const sub = await js.subscribe(pongSubject, opts);
//     (async () => {
//       for await (const m of sub) {
//         const jm = jc.decode(m.data);
//         console.log(`Received message: ${JSON.stringify(jm)}`);
//       }
//     })()
//       .then(() => {
//         nc.close();
//       })
//       .catch((err) => {
//         console.error(`Error: ${err}`);
//       });

//     await js.publish(registerSubject, jc.encode({ client_id: clientId }));
//     await new Promise((resolve) => setTimeout(resolve, 3000));
//     await js.publish(pingSubject, jc.encode({ msg: 'ping' }));
//   } catch (err: any) {
//     console.error(`Error: ${err}`);
//     if (err.code) {
//       console.error(`Error code: ${err.code}`);
//     }
//     if (err.chainedError) {
//       console.error(`Chained error: ${err.chainedError}`);
//     }
//   }
// }

// main();
