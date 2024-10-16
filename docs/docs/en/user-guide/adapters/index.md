# Network Adapters

Network Adapters in FastAgency provide a way to integrate your workflows with various communication protocols and interfaces. They allow you to **expose your workflows through different channels**, making it easier to interact with them from various client applications.

FastAgency uses **chainable network adapters** that can be easily combined to create **scalable**, **production-ready architectures** for serving your workflows. These adapters enable you to deploy your workflows in **distributed environments** and handle high volumes of requests.

## Why Use Network Adapters?

- **Production Deployment**: You can use network adapters to deploy agentic workflows in production settings. They provide a way for you to **scale up workloads** and deploy **fully distributed systems**, ensuring high availability and performance.
- **API Integration**: You can utilize an adapter like [**`FastAPIAdapter`**](../../api/fastagency/adapters/fastapi/FastAPIAdapter.md) to expose your workflows as a **REST API**. This allows other applications to interact with your workflows through standard HTTP requests, making it easy for you to integrate with existing systems.

- **Messaging Systems**: You can use message queue adapters like [**`NatsAdapter`**](../../api/fastagency/adapters/nats/NatsAdapter.md) to scale your workflows and handle high volumes of requests. This enables you to implement **distributed processing** and asynchronous communication between different components of your system, allowing for efficient resource utilization and improved performance.

## Available Adapters

### FastAPI

Use the [**`FastAPIAdapter`**](../../api/fastagency/adapters/fastapi/FastAPIAdapter.md) to serve your workflow using [**FastAPI**](https://fastapi.tiangolo.com/){target="_blank"} server. This setup allows you to work your workflows in multiple workers and serve them using the highly extensible and stable ASGI server.

[Learn more about **FastAPI** →](./fastapi/)

### Nats.io

Utilize the [**`NatsAdapter`**](../../api/fastagency/adapters/nats/NatsAdapter.md) to use [**NATS.io MQ**](https://nats.io/){target="_blank"} message broker for highly-scalable, production-ready setup. This interface is suitable for setups in VPN-s or, in combination with the [**`FastAPIAdapter`**](../api/fastagency/adapters/fastapi/FastAPIAdapter.md) to serve public workflows in an authenticated, secure manner.

[Learn more about **NATS.io** →](./nats/)
