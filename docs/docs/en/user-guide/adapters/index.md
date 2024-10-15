# Network Adapters

FastAgency can use chainable network adapters that can be used to easily create
scalable, production ready architectures for serving your workflows.

## Available Adapters

### FastAPI

Use the [**`FastAPIAdapter`**](../api/fastagency/adapters/fastapi/FastAPIAdapter.md) to serve your workflow using [**FastAPI**](https://fastapi.tiangolo.com/){target="_blank"} server. This setup allows you to work your workflows in multiple workers and serve them using the highly extensible and stable ASGI server.

[Learn more about **FastAPI** →](./fastapi/)

### Nats.io

Utilize the [**`NatsAdapter`**](../api/fastagency/adapters/nats/NatsAdapter.md) to use [**NATS.io MQ**](https://nats.io/){target="_blank"} message broker for highly-scalable, production-ready setup. This interface is suitable for setups in VPN-s or, in combination with the [**`FastAPIAdapter`**](../api/fastagency/adapters/fastapi/FastAPIAdapter.md) to serve public workflows in an authenticated, secure manner.

[Learn more about **NATS.io** →](./nats/)
