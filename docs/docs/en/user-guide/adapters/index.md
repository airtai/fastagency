# Network Adapters

Network Adapters in FastAgency provide a way to integrate your workflows with various [**communication protocols**](https://en.wikipedia.org/wiki/Communication_protocol){target="_blank"} and interfaces. They allow you to **expose your workflows through different channels**, making it easier to interact with them from various client applications.

FastAgency uses **chainable network adapters** that can be easily combined to create **scalable**, **production-ready architectures** for serving your workflows. These adapters enable you to deploy your workflows in **distributed environments** and handle high volumes of requests.

## Why Use Network Adapters?

- **Production Deployment**: You can use network adapters to deploy agentic workflows in production settings. They provide a way for you to **scale up workloads** and deploy fully [**distributed systems**](https://en.wikipedia.org/wiki/Distributed_computing){target="_blank"}, ensuring high availability and performance.
- **API Integration**: You can utilize an adapter like [**`FastAPIAdapter`**](../../api/fastagency/adapters/fastapi/FastAPIAdapter.md) to expose your workflows as a [**REST API**](https://en.wikipedia.org/wiki/REST){target="_blank"}. This allows other applications to interact with your workflows through standard [**HTTP**](https://en.wikipedia.org/wiki/HTTP){target="_blank"} requests, making it easy for you to integrate with existing systems.

- **Messaging Systems**: You can use [**message queue**](https://en.wikipedia.org/wiki/Message_queue){target="_blank"} adapters like [**`NatsAdapter`**](../../api/fastagency/adapters/nats/NatsAdapter.md) to scale your workflows and handle high volumes of requests. This enables you to implement [**distributed**](https://en.wikipedia.org/wiki/Distributed_computing){target="_blank"} processing and asynchronous communication between different components of your system, allowing for efficient resource utilization and improved performance.

## Available Adapters

### FastAPI

The [**`FastAPIAdapter`**](../../api/fastagency/adapters/fastapi/FastAPIAdapter.md) allows you to expose your FastAgency workflows as a [**REST API**](https://en.wikipedia.org/wiki/REST){target="_blank"} using the [**FastAPI**](https://fastapi.tiangolo.com/){target="_blank"} framework.

When to Use the [**`FastAPIAdapter`**](../../api/fastagency/adapters/fastapi/FastAPIAdapter.md):

- **Custom Client Applications**: If you want to build your **own client applications** in a different language, (e.g., [**HTML**](https://en.wikipedia.org/wiki/HTML){target="_blank"}/[**JavaScript**](https://en.wikipedia.org/wiki/JavaScript){target="_blank"}, [**Go**](https://go.dev/){target="_blank"}, [**Java**](https://www.java.com/en/){target="_blank"}, etc.), that interacts with your FastAgency workflows using [**REST API**](https://en.wikipedia.org/wiki/REST){target="_blank"} and [**WebSockets**](https://en.wikipedia.org/wiki/WebSocket){target="_blank"}.

- **Moderate User Demand**: This adapter is a good fit for scenarios where workflows need to be executed by [**multiple workers**](https://fastapi.tiangolo.com/deployment/server-workers/){target="_blank"} to efficiently handle higher machine load.

- **Simplified Production Setup**: This adapter is a good choice when you need a **simple and easy-to-manage** setup for [**deploying**](https://fastapi.tiangolo.com/deployment/){target="_blank"} FastAgency workflows as an [**ASGI**](https://asgi.readthedocs.io/en/latest/){target="_blank"} server in production.


[Learn more about **FastAPI adapter** →](./fastapi/index.md)

### FastAPI + Nats.io

Combining the [**`FastAPIAdapter`**](../../api/fastagency/adapters/fastapi/FastAPIAdapter.md) and [**`NatsAdapter`**](../../api/fastagency/adapters/nats/NatsAdapter.md) in FastAgency provides the most scalable setup. It harnesses the power of the [**FastAPI**](https://fastapi.tiangolo.com/){target="_blank"} framework to build and expose workflows as [**REST APIs**](https://en.wikipedia.org/wiki/REST){target="_blank"} while utilizing the [**Nats.io**](https://nats.io/){target="_blank"} message broker for scalable and asynchronous communication. This setup is **preferred** for running large workloads in production.

When to Use the [**`FastAPIAdapter`**](../../api/fastagency/adapters/fastapi/FastAPIAdapter.md) and [**`NatsAdapter`**](../../api/fastagency/adapters/nats/NatsAdapter.md) Together

- **High User Demand**: If you need to scale beyond what [**multiple workers**](https://fastapi.tiangolo.com/deployment/server-workers/){target="_blank"} of the [**FastAPIAdapter**](fastapi/index.md) can achieve, you can use [**Nats.io**](https://nats.io/){target="_blank"} with a [**message queue**](https://en.wikipedia.org/wiki/Message_queue){target="_blank"} and [**multiple workers**](https://fastapi.tiangolo.com/deployment/server-workers/){target="_blank"} to consume and produce messages. This distributed message-queue architecture allows scaling not only across multiple workers but also across multiple machines and clusters.

- [**Observability**](https://en.wikipedia.org/wiki/Observability_(software)){target="_blank"}: If you need the ability to **audit workflow executions** both in realtime and retrospectively, the [**`NatsAdapter`**](../../api/fastagency/adapters/nats/NatsAdapter.md) provides the necessary infrastructure to enable this feature.

- **Security features of FastAPI**: If you want to leverage the [**security features**](https://fastapi.tiangolo.com/tutorial/security){target="_blank"} of FastAPI, such as authentication, authorization, along with the [**distributed architecture**](https://en.wikipedia.org/wiki/Distributed_computing){target="_blank"} of NATS, this setup is the most suitable option. Please check the [**securing your FastAPIAdapter**](fastapi/security.md) documentation for more information.

[Learn more about **FastAPI + NATS.io adapter** →](./fastapi_nats/index.md)

### Nats.io

The [**`NatsAdapter`**](../../api/fastagency/adapters/nats/NatsAdapter.md) in FastAgency enables seamless integration of your workflows with the [**Nats.io MQ**](https://nats.io/){target="_blank"} message broker, providing a scalable and flexible solution for building [**distributed**](https://en.wikipedia.org/wiki/Distributed_computing){target="_blank"} applications.

When to Use the [**`NatsAdapter`**](../../api/fastagency/adapters/nats/NatsAdapter.md):

- **High User Demand**: If you need to scale beyond what [**multiple workers**](https://fastapi.tiangolo.com/deployment/server-workers/){target="_blank"} of the [**FastAPIAdapter**](fastapi/index.md) can achieve, you can use [**Nats.io**](https://nats.io/){target="_blank"} with a [**message queue**](https://en.wikipedia.org/wiki/Message_queue){target="_blank"} and [**multiple workers**](https://fastapi.tiangolo.com/deployment/server-workers/){target="_blank"} to consume and produce messages. This distributed message-queue architecture allows scaling not only across multiple workers but also across multiple machines and clusters.

- [**Observability**](https://en.wikipedia.org/wiki/Observability_(software)){target="_blank"}: If you need the ability to **audit workflow executions** both in realtime and retrospectively, the [**`NatsAdapter`**](../../api/fastagency/adapters/nats/NatsAdapter.md) provides the necessary infrastructure to enable this feature.


[Learn more about **NATS.io adapter** →](./nats/index.md)
