from fastapi import FastAPI

from .base import FastAPIProvider, NatsProvider

nats_provider = NatsProvider.Client(url="nats://localhost:4222")

provider = FastAPIProvider(
    discovery_path="/autogen",
    create_path="/workflow/create",
    no_workers=10,
    provider=nats_provider,
)

# in case of FastAPI
app = FastAPI(lifespan=provider.lifespan())


# ... define routes
@app.get("/fastagency/workflow/create")
def create_workflow():
    return provider.start_workflow("simple_learning", "Hello, teacher!", "session_id")

@app.get("/fastagency/discovery")
def discovery():
    ...

# Run with the following command:
# uvicorn main_fastapi:app --reload
