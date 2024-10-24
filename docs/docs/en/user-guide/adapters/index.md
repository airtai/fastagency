# Network Adapters

Network Adapters in FastAgency provide a way to integrate your workflows with various [**communication protocols**](https://en.wikipedia.org/wiki/Communication_protocol){target="_blank"} and interfaces. They allow you to **expose your workflows through different channels**, making it easier to interact with them from various client applications.

FastAgency uses **chainable network adapters** that can be easily combined to create **scalable**, **production-ready architectures** for serving your workflows. These adapters enable you to deploy your workflows in **distributed environments** and handle high volumes of requests.

## Why Use Network Adapters?

- [**Production Deployment**](https://fastapi.tiangolo.com/deployment){target="_blank"}: You can use network adapters to deploy agentic workflows in production settings. They provide a way for you to **scale up workloads** and deploy fully [**distributed systems**](https://en.wikipedia.org/wiki/Distributed_computing){target="_blank"}, ensuring high availability and performance.
- **API Integration**: You can utilize an adapter like [**`FastAPIAdapter`**](../../api/fastagency/adapters/fastapi/FastAPIAdapter.md) to expose your workflows as a [**REST API**](https://en.wikipedia.org/wiki/REST){target="_blank"}. This allows other applications to interact with your workflows through standard [**HTTP**](https://en.wikipedia.org/wiki/HTTP){target="_blank"} requests, making it easy for you to integrate with existing systems.

- **Messaging Systems**: You can use [**message queue**](https://en.wikipedia.org/wiki/Message_queue){target="_blank"} adapters like [**`NatsAdapter`**](../../api/fastagency/adapters/nats/NatsAdapter.md) to scale your workflows and handle high volumes of requests. This enables you to implement [**distributed**](https://en.wikipedia.org/wiki/Distributed_computing){target="_blank"} processing and asynchronous communication between different components of your system, allowing for efficient resource utilization and improved performance.

## Available Adapters

### FastAPI

Use the [**`FastAPIAdapter`**](../../api/fastagency/adapters/fastapi/FastAPIAdapter.md) to serve your FastAgency workflows as a [**REST API**](https://en.wikipedia.org/wiki/REST){target="_blank"} using the [**FastAPI**](https://fastapi.tiangolo.com/){target="_blank"} framework. This setup allows you to work your workflows in [**multiple workers**](https://fastapi.tiangolo.com/deployment/server-workers/){target="_blank"} and serve them using the highly extensible and stable [**ASGI**](https://asgi.readthedocs.io/en/latest/){target="_blank"} server.

When to Use the [**`FastAPIAdapter`**](../../../api/fastagency/adapters/fastapi/FastAPIAdapter.md):

- **Custom Client Applications**: If you want to build your **own client applications** in a language other than Python, (e.g., [**HTML**](https://en.wikipedia.org/wiki/HTML){target="_blank"}/[**JavaScript**](https://en.wikipedia.org/wiki/JavaScript){target="_blank"}), that interacts with your FastAgency workflows using [**REST API**](https://en.wikipedia.org/wiki/REST){target="_blank"} and [**WebSockets**](https://en.wikipedia.org/wiki/WebSocket){target="_blank"}.

- **Moderate User Demand**: This adapter is a good fit for scenarios where workflows need to be executed by [**multiple workers**](https://fastapi.tiangolo.com/deployment/server-workers/){target="_blank"} to efficiently handle higher machine load.

- **Simplified Production Setup**: This adapter is a good choice when you need a **simple and easy-to-manage** setup for [**deploying**](https://fastapi.tiangolo.com/deployment/){target="_blank"} FastAgency workflows as an [**ASGI**](https://asgi.readthedocs.io/en/latest/){target="_blank"} server in production.


[Learn more about **FastAPI adapter** →](./fastapi/index.md)

### FastAPI + Nats.io

The [**`FastAPIAdapter`**](../../api/fastagency/adapters/fastapi/FastAPIAdapter.md) + [**`NatsAdapter`**](../../api/fastagency/adapters/nats/NatsAdapter.md) in FastAgency offers the most scalable setup by combining the power of the [**FastAPI**](https://fastapi.tiangolo.com/){target="_blank"} framework for building and exposing workflows as REST APIs with the [**NATS.io MQ**](https://nats.io/){target="_blank"} message broker for scalable and asynchronous communication. This setup is the preferred way for running large workloads in production.

#### When to Use the FastAPI + NATS.io Adapter

- **Custom Client Applications**: If you want to build your **own client applications** that interact with your FastAgency workflows using REST APIs, this adapter provides greater flexibility and control over the client-side implementation.
- **High User Demand**: When your application needs to handle a large number of users or messages and requires high scalability, the FastAPI + NATS Adapter is an excellent choice. It is well-suited for building **scalable custom chat applications for larger companies or external customers**.
- **Conversation Auditing**: If you need the ability to **audit conversations**, the NATS Adapter provides the necessary infrastructure to enable this feature.

[Learn more about **FastAPI + NATS.io adapter** →](./fastapi_nats/index.md)

### Nats.io

Utilize the [**`NatsAdapter`**](../../api/fastagency/adapters/nats/NatsAdapter.md) to use [**NATS.io MQ**](https://nats.io/){target="_blank"} message broker for highly-scalable, production-ready setup.

#### When to Use the [**`NatsAdapter`**](../../api/fastagency/adapters/nats/NatsAdapter.md)

- **Default Client Application**: If you prefer using the **default Mesop client** provided by FastAgency without the need to build your own client application.

- **High User Demand**: When your application requires **high scalability** to handle a large number of users or messages, and you are comfortable with a more complex production setup involving a message broker. For example, it's well-suited for building a **scalable chat application** for a larger company or external customers.

- **Conversation Auditing**: If you need the ability to **audit conversations**, the NATS Adapter provides the necessary infrastructure to enable this feature.


[Learn more about **NATS.io adapter** →](./nats/index.md)
