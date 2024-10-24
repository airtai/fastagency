from os import environ

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from fastagency.adapters.fastapi import FastAPIAdapter
from fastagency.adapters.nats import NatsAdapter

html = """
<!DOCTYPE html>
<html>
   <head>
      <title>FastAgency Chat App</title>
   </head>
   <body>
      <h1>FastAgency Chat App</h1>
      <div id="workflows"></div>
      <ul id="messages"></ul>
      <script>
         const API_URL = 'http://127.0.0.1:8008/fastagency';
         const WS_URL = 'ws://127.0.0.1:8008/fastagency/ws'; // nosemgrep
         let socket;

         async function fetchWorkflows() {
             const response = await fetch(`${API_URL}/discovery`);
             const workflows = await response.json();
             const container = document.getElementById('workflows');
             workflows.forEach(workflow => {
                 const button = document.createElement('button');
                 button.textContent = workflow.description;
                 button.onclick = () => startWorkflow(workflow.name);
                 container.appendChild(button);
             });
         }

         async function startWorkflow(name) {
             const payload = {
                 workflow_name: name,
                 workflow_uuid: generateUUID(),
                 user_id: null, // Set to null for single-user applications; otherwise, provide the appropriate user ID
                 params: {}
             };
             const response = await fetch(`${API_URL}/initiate_workflow`, {
                 method: 'POST',
                 headers: { 'Content-Type': 'application/json' },
                 body: JSON.stringify(payload)
             });
             const workflowJson = await response.json();
             connectWebSocket(workflowJson);
         }

         function connectWebSocket(workflowJson) {
             socket = new WebSocket(WS_URL);
             socket.onopen = () => {
                 const initMessage = {
                     name: workflowJson.name,
                     workflow_uuid: workflowJson.workflow_uuid,
                     user_id: workflowJson.user_id,
                     params: {}
                 };
                 socket.send(JSON.stringify(initMessage));
             };
             socket.onmessage = (event) => handleMessage(JSON.parse(event.data));
         }

         function handleMessage(message) {
             const messagesList = document.getElementById('messages');
             const li = document.createElement('li');
             if (message.type === 'text_input') {
                 const response = prompt(message.content.prompt);
                 socket.send(response);
                 li.textContent = `${message.sender} -> ${message.recipient}: ${message.content.prompt}`;
             } else {
                 li.textContent = `${message.sender} -> ${message.recipient}: ${message.content?.body || message?.type || JSON.stringify(message)}`;
             }
             messagesList.appendChild(li);
         }

         fetchWorkflows();

         // Helper function for generating UUID
         function generateUUID() {
            return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
                if (c === 'x') {
                return (Math.random() * 16 | 0).toString(16);
                } else {
                return (Math.random() * 16 | 0 & 0x3 | 0x8).toString(16);
                }
            });
         }
      </script>
   </body>
</html>
"""

nats_url = environ.get("NATS_URL", "nats://localhost:4222")
nats_user: str = "fastagency"
nats_password: str = environ.get("FASTAGENCY_NATS_PASSWORD", "fastagency_nats_password")  # type: ignore[assignment]

provider = NatsAdapter.create_provider(
    nats_url=nats_url, user=nats_user, password=nats_password
)

adapter = FastAPIAdapter(
    provider=provider,
)

# app = FastAPI(lifespan=provider.lifespan)
app = FastAPI()
app.include_router(adapter.router)


@app.get("/")
async def get() -> HTMLResponse:
    return HTMLResponse(html)


# start the provider with the following command
# uvicorn main_2_fastapi_custom_client:app --host 0.0.0.0 --port 8008 --reload
