# Securing the FastAPIAdapter

When exposing your FastAgency workflows using the [**`FastAPIAdapter`**](../../../api/fastagency/adapters/fastapi/FastAPIAdapter.md), it's crucial to ensure the security of your API. Implementing proper security practices will protect your data, workflows, and client applications from unauthorized access, attacks, and data breaches.

This section will demonstrate how to secure your [**`FastAPIAdapter`**](../../../api/fastagency/adapters/fastapi/FastAPIAdapter.md).

## Authentication
Authentication is the process of verifying who a user is. For securing your [**`FastAPIAdapter`**](../../../api/fastagency/adapters/fastapi/FastAPIAdapter.md), we recommend using [OAuth2](https://oauth.net/2/){target="_blank"} with password flow or API keys. In this section, we’ll demonstrate how to use the following security variations of [OAuth2](https://oauth.net/2/){target="_blank"} with [FastAPI](https://fastapi.tiangolo.com/){target="_blank"}:

- [simple OAuth2](https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/){target="_blank"}, and

- [OAuth2 using JWT tokens](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/){target="_blank"}.

## Example: OAuth2 Password Flow

Lets first take a look at the full code on how to add the [OAuth2](https://oauth.net/2/){target="_blank"} security to your [**`FastAPIAdapter`**](../../../api/fastagency/adapters/fastapi/FastAPIAdapter.md), and then go through the code step by step.

Here’s the full code on how you can add [OAuth2](https://oauth.net/2/){target="_blank"} password flow to your [**`FastAPIAdapter`**](../../../api/fastagency/adapters/fastapi/FastAPIAdapter.md):

=== "simple OAuth2"

    <details>
        <summary>main.py</summary>
        ```python
        {!> docs_src/user_guide/adapters/fastapi/security/main_1_simple.py !}
        ```
    </details>


=== "OAuth2 using JWT tokens"

    <details>
        <summary>main.py</summary>
        ```python
        {!> docs_src/user_guide/adapters/fastapi/security/main_1_jwt.py !}
        ```
    </details>



The main module imports the workflow from `workflows.py`, so make sure you have this file saved in the same directory as the `main.py`.

<details>
    <summary>workflows.py</summary>
    ```python
    {!> docs_src/user_guide/adapters/fastapi/security/workflows.py !}
    ```
</details>

The project structure should look like this:
```
secured_fastapi_adapter
+-- __init__.py
+-- main.yml.py
+-- workflows.py
```

You can now start your secured adapter using the following command:

```
uvicorn secured_fastapi_adapter.main:app --host 0.0.0.0 --port 8008
```

Now, lets go through the steps on how to build the [OAuth2](https://oauth.net/2/){target="_blank"} security and add it to your FastAPI provider.

### Step 0: Install dependencies

=== "simple OAuth2"

    ```console
    pip install "fastagency[autogen,mesop,fastapi,server]"
    ```


=== "OAuth2 using JWT tokens"

    To use JWT tokens, you need to install [PyJWT](https://pyjwt.readthedocs.io/en/stable/) and [passlib](https://passlib.readthedocs.io/en/stable/) in addition to fastagency.

    ```console
    pip install "fastagency[autogen,mesop,fastapi,server]"
    pip install PyJWT
    pip install "passlib[bcrypt]"
    ```

This command installs FastAgency with support for both the Console and [Mesop](https://google.github.io/mesop/)
interfaces for [AutoGen](https://microsoft.github.io/autogen/) workflows, but with FastAPI both serving input requests
and running workflows.

### Step 1: Imports

=== "simple OAuth2"

    ```python
        {!> docs_src/user_guide/adapters/fastapi/security/main_1_simple.py [ln:1-10]!}
    ```

=== "OAuth2 using JWT tokens"

    ```python
        {!> docs_src/user_guide/adapters/fastapi/security/main_1_jwt.py [ln:1-14]!}
    ```

- [**`AutoGenWorkflows`**](../../../api/fastagency/runtimes/autogen/AutoGenWorkflows.md): Manages and registers workflows. Here, the simple_workflow is registered under the name "simple_learning".

- [**`FastAPIAdapter`**](../../../api/fastagency/adapters/fastapi/FastAPIAdapter.md): We'll attach the adapter to the FastAPI app. It exposes the workflows as REST APIs.


### Step 2: Initial Setup
We start by defining the [`FastAPI` app](https://fastapi.tiangolo.com/reference/fastapi/){target="_blank"}, setting up the [**`AutoGenWorkflows`**](../../../api/fastagency/runtimes/autogen/AutoGenWorkflows.md) object, and registering a simple workflow (simple_learning) for the adapter.

=== "simple OAuth2"

    ```python
        {!> docs_src/user_guide/adapters/fastapi/security/main_1_simple.py [ln:12-19]!}
    ```

=== "OAuth2 using JWT tokens"

    ```python
        {!> docs_src/user_guide/adapters/fastapi/security/main_1_jwt.py [ln:16-23]!}
    ```


### Step 3: Mock Database Setup
This step sets up a mock database with two users (johndoe and alice). This is a simplified user store for the example, where each user has attributes like username, email, and hashed_password.

=== "simple OAuth2"

    ```python
    {!> docs_src/user_guide/adapters/fastapi/security/main_1_simple.py [ln:26-41]!}
    ```


=== "OAuth2 using JWT tokens"

    ```python
    {!> docs_src/user_guide/adapters/fastapi/security/main_1_jwt.py [ln:37-45]!}
    ```
    You can see in this example that the password is not stored as a plaintext but as a hash in the database, to find out more on how this hash is generated, and more details about securing your app with OAuth2 and hashed passwords, please visit [OAuth2 using JWT tokens FastAPI tutorial](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/){target="_blank"}.

- `fake_users_db`: A dictionary that represents a mock database of users. Each user has attributes like `hashed_password`, `disabled` (for checking active users), and `user_id` (which we will use for authorization).

### Step 4: OAuth2 Authentication Setup
Here we configure OAuth2 with password flow and token-based authentication. This ensures that users authenticate with a username and password, and the app generates a token.

=== "simple OAuth2"

    ```python
    {!> docs_src/user_guide/adapters/fastapi/security/main_1_simple.py [ln:43-47]!}
    ```

    `OAuth2PasswordBearer`: This is used to handle token-based authentication. `tokenUrl="token"` indicates that users will obtain a token by calling the `/token` endpoint.

    `fake_hash_password`: A simple mock function to simulate password hashing.

=== "OAuth2 using JWT tokens"

    ```python
    {!> docs_src/user_guide/adapters/fastapi/security/main_1_jwt.py [ln:48-50]!}
    ```

    `OAuth2PasswordBearer`: This is used to handle token-based authentication. `tokenUrl="token"` indicates that users will obtain a token by calling the `/token` endpoint.

    `pwd_context`: `CryptContext` which will be used for password hash verification.

### Step 5: User Authentication Logic
This step simulates user lookup, token decoding, and user validation. The token received in API requests is decoded to get the user, and the user’s information is validated for authorization.

=== "simple OAuth2"

    ```python
    {!> docs_src/user_guide/adapters/fastapi/security/main_1_simple.py [ln:50-91]!}
    ```

    - `User and UserInDB`: These Pydantic models represent user data. UserInDB extends User by adding a hashed_password field for password comparison.

    - `get_user`: This function retrieves user data from `fake_users_db`.

    - `fake_decode_token`: Simulates the process of decoding a token to extract user information (in this mock, the token is just the username).


=== "OAuth2 using JWT tokens"

    ```python
    {!> docs_src/user_guide/adapters/fastapi/security/main_1_jwt.py [ln:53-109]!}
    ```

    - `User and UserInDB`: These Pydantic models represent user data. UserInDB extends User by adding a hashed_password field for password comparison.

    - `get_user`: This function retrieves user data from `fake_users_db`.

    - `verify_password`: Verifies the user paswword by comparing it to the password hash in the `fake_users_db`

### Step 6: OAuth2 Token Login Endpoint
This step defines the `/token` endpoint where users submit their username and password to receive an authentication token. The system checks if the password matches before generating the token.

=== "simple OAuth2"

    ```python
    {!> docs_src/user_guide/adapters/fastapi/security/main_1_simple.py [ln:94-104]!}
    ```

    - `/token`: This endpoint handles user login. If the username and password match, it returns a token in the form of the username. Otherwise, an error is returned.


=== "OAuth2 using JWT tokens"

    ```python
    {!> docs_src/user_guide/adapters/fastapi/security/main_1_jwt.py [ln:112-147]!}
    ```

    - `create_access_token`: Generates a JSON Web Token (JWT) that will be returned to the user after authenticating through the `/token` endpoint
    - `/token`: This endpoint handles user login. If the username and password match, it returns a token in the form of a JWT. Otherwise, an error is returned.

### Step 7: Securing Routes with OAuth2
Here we secure the FastAPI routes by requiring the user to pass an OAuth2 token to authenticate and authorize requests.

=== "simple OAuth2"

    ```python
    {!> docs_src/user_guide/adapters/fastapi/security/main_1_simple.py [ln:75-91]!}
    ```


=== "OAuth2 using JWT tokens"

    ```python
    {!> docs_src/user_guide/adapters/fastapi/security/main_1_jwt.py [ln:84-109]!}
    ```

- `get_current_user`: This function extracts the token from the request, decodes it, and returns the user object if valid. If the token is invalid, a 401 error is returned.

- `get_current_active_user`: It checks whether the user account is active `(disabled = False)`, raising an error if the user is inactive.

### Step 8: Custom Client ID Generation
This step extracts the user’s user_id from the current authenticated user and provides it to the adapter. This will allow syncing client information during workflow interactions.

=== "simple OAuth2"

    ```python
    {!> docs_src/user_guide/adapters/fastapi/security/main_1_simple.py [ln:112-115]!}
    ```

=== "OAuth2 using JWT tokens"

    ```python
    {!> docs_src/user_guide/adapters/fastapi/security/main_1_jwt.py [ln:155-158]!}
    ```

`get_user_id`: Returns the user_id of the authenticated user, which is later used for authorization in the workflows.

### Step 9: Connecting the Adapter and Securing It
Finally, we connect the [**`FastAPIAdapter`**](../../../api/fastagency/adapters/fastapi/FastAPIAdapter.md) to the FastAPI app. The get_user_id function is passed as a security dependency, ensuring that every internal API call is secured.

=== "simple OAuth2"

    ```python
    {!> docs_src/user_guide/adapters/fastapi/security/main_1_simple.py [ln:117-118]!}
    ```

=== "OAuth2 using JWT tokens"

    ```python
    {!> docs_src/user_guide/adapters/fastapi/security/main_1_jwt.py [ln:159-162]!}
    ```

`get_user_id`: This function ensures that the `user_id` of the authenticated user is passed with every internal request, securing the workflows exposed by the adapter.

### Step 10: Workflow Listing Endpoint
We add an optional `/` endpoint to list the available workflows, which can be useful for understanding what workflows are currently available in the [**`FastAPIAdapter`**](../../../api/fastagency/adapters/fastapi/FastAPIAdapter.md).

=== "simple OAuth2"

    ```python
    {!> docs_src/user_guide/adapters/fastapi/security/main_1_simple.py [ln:121-123]!}
    ```


=== "OAuth2 using JWT tokens"

    ```python
    {!> docs_src/user_guide/adapters/fastapi/security/main_1_jwt.py [ln:164-166]!}
    ```

`/`: Lists the available workflows and their descriptions for easier access and understanding of what the API offers.

### Final Explanation

In this setup:

 - Authentication is handled using OAuth2, with token generation via a `/token` endpoint.

 - User information is stored in a mock database, and token-based authentication ensures that only valid users can interact with the workflows.

 - The `get_user_id` function is the central security mechanism, ensuring that each user’s actions are tracked and authorized via their `user_id`.

 - By attaching the `get_user_id` function to the [**`FastAPIAdapter`**](../../../api/fastagency/adapters/fastapi/FastAPIAdapter.md), we effectively secure all the internal API calls exposed by the workflows, providing a scalable and consistent approach to authorization and client sync.

## Implementing and connecting a simple client to secured FastAPIAdapter

Now we will implement a client that can connect to your secured [**`FastAPIAdapter`**](../../../api/fastagency/adapters/fastapi/FastAPIAdapter.md). Here is the full code of the client which you can run using `python simple_client.py` in your console.

<details>
    <summary>simple_client.py</summary>
    ```python
    {!> docs_src/user_guide/adapters/fastapi/security/simple_client.py !}
    ```
</details>

Now let's do a step-by-step breakdown of the code, focusing on the OAuth2 token acquisition and WebSocket security. We'll explain each part with relevant code snippets and describe how the `ConsoleUI` is used for simplicity, but note that you can implement custom message processing logic.

### Step 1: Authenticate and Get OAuth2 Token

The first part of the process is obtaining an access token by authenticating with the FastAPI server using OAuth2.

```python
    {!> docs_src/user_guide/adapters/fastapi/security/simple_client.py [ln:16-26]!}
```

- **What happens**:
    - The `CREDENTIALS` dictionary holds the username and password for a user (in this case, `"johndoe"` and `"secret"`).
    - The `get_oauth_token()` function sends a POST request to the FastAPI authentication endpoint (`/token`) with these credentials.
    - If the authentication is successful, the FastAPI server returns a token as the `access_token`. This token will be used in the headers for subsequent requests.

- **Key Points**:
    - This token secures the API calls and WebSocket connections by proving the user’s identity.
    - The `raise_for_status()` ensures any HTTP error (e.g., wrong credentials) will raise an exception, helping with debugging.

### Step 2: Initiate the Workflow

After obtaining the token, we initiate a workflow by sending a POST request to the server, passing the token in the headers for authorization.

```python
    {!> docs_src/user_guide/adapters/fastapi/security/simple_client.py [ln:29-41]!}
```

- **What happens**:
    - This function constructs a payload that includes the workflow name, a UUID (in this case, hardcoded to `"1234"`), and some parameters (a message saying `"Hello"`).
    - It sends a POST request to the `/fastagency/initiate_workflow` endpoint, which triggers the desired workflow on the server.
    - The OAuth2 token is added in the headers for authorization: `"Authorization": f"Bearer {token}"`.

- **Key Points**:
    - The workflow can have dynamic parameters like user ID and message. You can modify this payload to fit your specific workflow.
    - The server returns an initial payload that will be used to start communication over WebSockets.

### Step 3: Establish WebSocket Connection

Now, we use the WebSocket protocol to establish a real-time connection with the FastAPI server and handle the workflow’s communication.

```python
    {!> docs_src/user_guide/adapters/fastapi/security/simple_client.py [ln:44-51]!}
```

- **What happens**:
    - The WebSocket connection is made to the FastAPI WebSocket endpoint (`/fastagency/ws`).
    - The `Authorization` header with the `Bearer` token ensures that the WebSocket connection is secured and authenticated.
    - The `initial_payload` obtained from the previous step is sent to the WebSocket server to start the workflow.

- **Key Points**:
    - The WebSocket connection is protected by the OAuth2 token, just like the HTTP requests.
    - The `ConsoleUI` is used here to keep things simple, but this UI can be replaced with a custom implementation for processing incoming messages from the server.

### Step 4: Handling WebSocket Messages

Once the WebSocket connection is established, the client listens for messages from the server, processes them, and sends appropriate responses if required.

```python
    {!> docs_src/user_guide/adapters/fastapi/security/simple_client.py [ln:53-66]!}
```

- **What happens**:
    - The client continuously listens for messages using `await websocket.recv()`.
    - The received messages are processed by the `ConsoleUI` (or custom message handling logic).
    - If the server sends an `AskingMessage` (a message requesting input), the client responds appropriately.
    - When the workflow is completed (`WorkflowCompleted`), the loop breaks, and the connection is closed.

- **Key Points**:
    - The `ConsoleUI` simplifies the example by handling basic message processing. It can be replaced with custom UI logic for more complex workflows.
    - The `asyncify` decorator is used to make the `ui.process_message` function non-blocking, allowing the program to handle other asynchronous tasks while waiting for user input.

### Step 5: Running the Workflow

Finally, the entire process is orchestrated in the `main()` function, which ties everything together.

```python
    {!> docs_src/user_guide/adapters/fastapi/security/simple_client.py [ln:69-82]!}
```

- **What happens**:
    - The `main()` function first authenticates the user to get the OAuth2 token.
    - It then initiates the workflow by sending the appropriate request and gets the initial WebSocket payload.
    - Finally, it handles the WebSocket communication, processing messages and interacting with the workflow in real-time.

### Summary

- **Token Acquisition**: OAuth2 token is obtained via the `/token` endpoint, securing both API and WebSocket interactions.
- **WebSocket Security**: WebSocket communication is secured by passing the OAuth2 token in the `Authorization` header.
- **Message Processing**: The `ConsoleUI` is used for simplicity, but you can implement your own message-handling logic to interact with the workflow.

By using OAuth2 for authentication and WebSockets for real-time communication, this example demonstrates how you can build a secure, interactive client to communicate with a FastAPI-based workflow system.
