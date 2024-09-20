# Import necessary modules
# from fastagency.studio.io import IONats
from fastapi import FastAPI, Request, APIRouter
from pydantic import BaseModel
from fastagency.studio.io.ionats import app as nats_faststream_app, broker as nats_broker

from contextlib import asynccontextmanager
from typing import AsyncGenerator


class InputRequestModel(BaseModel):
    prompt: str
    is_password: bool

class InputResponseModel(BaseModel):
    msg: str

class TerminateModel(BaseModel):
    msg: str = "Chat completed."

class ErrorResponseModel(BaseModel):
    msg: str

# Define the FastAPIUI class
class FastAPIUI:
    def __init__(self):
        self.router = APIRouter()
        # self.ionats = IONats()

        # Define routes
        self.router.post("/input")(self.handle_input)
        self.router.post("/terminate")(self.handle_terminate)
        self.router.post("/error")(self.handle_error)

    async def handle_input(self, input_request: InputRequestModel) -> InputResponseModel:
        # Process input using IONats
        # response = await self.ionats.process_input(input_request.prompt, input_request.is_password)
        response = InputResponseModel(msg=f"response for {input_request.prompt}")
        return response

    async def handle_terminate(self, terminate_request: TerminateModel) -> TerminateModel:
        # Process termination using IONats
        # await self.ionats.terminate()
        return terminate_request

    async def handle_error(self, error_request: ErrorResponseModel) -> ErrorResponseModel:
        # Log error using IONats
        # await self.ionats.log_error(error_request.msg)
        return error_request
    
    @asynccontextmanager
    async def lifespan(self, app) -> AsyncGenerator[None, None]:
        # async with nats_faststream_app.lifespan():
        #     yield
        print("At FastAPIUI lifespan")
        async with nats_broker:
            await nats_broker.start()
            try:
                yield
            finally:
                await nats_broker.close()

