import asyncio
import json
from typing import Any

import requests
import websockets
from asyncer import asyncify

from fastagency.messages import AskingMessage, IOMessage, WorkflowCompleted
from fastagency.ui.console import ConsoleUI

# API base URL
FASTAGENCY_URL = "http://localhost:8008"

# User credentials
CREDENTIALS = {
    "username": "johndoe",
    "password": "secret" # pragma: allowlist secret
}

# Function to authenticate and get the OAuth token
def get_oauth_token() -> str:
    """Authenticate the user and return the access token."""
    response = requests.post(f"{FASTAGENCY_URL}/token", data=CREDENTIALS)
    response.raise_for_status()  # Ensure we handle errors
    return response.json().get("access_token") # type: ignore

# Function to initiate the workflow
def initiate_workflow(token: str) -> dict[str, Any]:
    """Initiate the workflow and return the initial payload."""
    payload = {
        "workflow_name": "simple_learning",
        "workflow_uuid": "1234",  # You can generate this dynamically
        "user_id": None,
        "params": {"message": "Hello"}
    }

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{FASTAGENCY_URL}/fastagency/initiate_workflow", json=payload, headers=headers)
    response.raise_for_status()  # Ensure we handle errors
    return response.json() # type: ignore

# Function to handle WebSocket communication
async def websocket_workflow(token: str, initial_payload: dict[str, Any]) -> None:
    """Establish a WebSocket connection and handle the workflow interaction."""
    websocket_url = f"ws{FASTAGENCY_URL[4:]}/fastagency/ws"
    ui = ConsoleUI()  # Initialize the UI for handling user interaction

    async with websockets.connect(websocket_url, extra_headers={"Authorization": f"Bearer {token}"}) as websocket:
        # Send the initial payload to start the workflow
        await websocket.send(json.dumps(initial_payload))

        while True:
            # Receive messages from the WebSocket server
            response = await websocket.recv()
            message = IOMessage.create(**json.loads(response))

            # Process the received message and interact with the UI
            result = await asyncify(ui.process_message)(message)

            # Respond if the message requires further input
            if isinstance(message, AskingMessage) and result is not None:
                await websocket.send(result)
            elif isinstance(message, WorkflowCompleted):
                # Exit the loop when the workflow is completed
                break

# Main function to run the workflow
async def main() -> None:
    """Main function to orchestrate the workflow."""
    # Step 1: Authenticate to get the OAuth2 token
    token = get_oauth_token()

    # Step 2: Initiate the workflow and get the initial payload
    initial_payload = initiate_workflow(token)

    # Step 3: Handle WebSocket interaction
    await websocket_workflow(token, initial_payload)

if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())
