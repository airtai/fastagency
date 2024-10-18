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

#### When to Use the [**`FastAPIAdapter`**](../../api/fastagency/adapters/fastapi/FastAPIAdapter.md)

- **Custom Client Applications**: If you want to build your **own client applications** that interact with your FastAgency workflows using REST APIs, this adapter provides greater flexibility and control over the client-side implementation.
- **Moderate User Demand**: The FastAPI Adapter is a good fit for scenarios with **moderate user request volume**. For example, it's well-suited for a medium-sized company developing an internal custom chat application.
- **Simplified Production Setup**: Choose this adapter if you need a **simple and easy-to-manage** production setup for deploying your FastAgency workflows as a REST API.


[Learn more about **FastAPI adapter** →](./fastapi/)

### FastAPI + Nats.io

The [**`FastAPIAdapter`**](../../api/fastagency/adapters/fastapi/FastAPIAdapter.md) + [**`NatsAdapter`**](../../api/fastagency/adapters/nats/NatsAdapter.md) in FastAgency offers the most scalable setup by combining the power of the [**FastAPI**](https://fastapi.tiangolo.com/){target="_blank"} framework for building and exposing workflows as REST APIs with the [**NATS.io MQ**](https://nats.io/){target="_blank"} message broker for scalable and asynchronous communication. This setup is the preferred way for running large workloads in production.

#### When to Use the FastAPI + NATS.io Adapter

- **Custom Client Applications**: If you want to build your **own client applications** that interact with your FastAgency workflows using REST APIs, this adapter provides greater flexibility and control over the client-side implementation.
- **High User Demand**: When your application needs to handle a large number of users or messages and requires high scalability, the FastAPI + NATS Adapter is an excellent choice. It is well-suited for building **scalable custom chat applications for larger companies or external customers**.
- **Conversation Auditing**: If you need the ability to **audit conversations**, the NATS Adapter provides the necessary infrastructure to enable this feature.

[Learn more about **FastAPI + NATS.io adapter** →](./fastapi_nats/)

### Nats.io

Utilize the [**`NatsAdapter`**](../../api/fastagency/adapters/nats/NatsAdapter.md) to use [**NATS.io MQ**](https://nats.io/){target="_blank"} message broker for highly-scalable, production-ready setup.

#### When to Use the [**`NatsAdapter`**](../../api/fastagency/adapters/nats/NatsAdapter.md)

- **Default Client Application**: If you prefer using the **default Mesop client** provided by FastAgency without the need to build your own client application.

- **High User Demand**: When your application requires **high scalability** to handle a large number of users or messages, and you are comfortable with a more complex production setup involving a message broker. For example, it's well-suited for building a **scalable chat application** for a larger company or external customers.

- **Conversation Auditing**: If you need the ability to **audit conversations**, the NATS Adapter provides the necessary infrastructure to enable this feature.


[Learn more about **NATS.io adapter** →](./nats/)
