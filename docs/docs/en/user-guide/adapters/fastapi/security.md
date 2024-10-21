# Securing the FastAPI Adapter

When exposing your FastAgency workflows using the FastAPI Adapter, it's crucial to ensure the security of your API. Implementing proper security practices will protect your data, workflows, and client applications from unauthorized access, attacks, and data breaches.

This section will demonstrate how to secure your FastAPI adapter.

## Authentication
Authentication is the process of verifying who a user is. For securing your FastAPI Adapter, we recommend using OAuth2 with password flow or API keys. In this section, we’ll demonstrate how to use OAuth2 with FastAPI.

## Example: OAuth2 Password Flow

Lets first take a look at the full code on how to add the OAuth2 security to your FastAPI Adapter, and then go through the code step by step.

Here’s the full code on how you can add OAuth2 password flow to your FastAPI Adapter:

<details>
    <summary>main.py</summary>
    ```python
    {!> docs_src/user_guide/adapters/fastapi/security/main_1_fastapi.py !}
    ```
</details>

The main module imports the workflow from `workflows.py`, so make sure you have this file saved in the sam e directory as the `main.py`.

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

Now, lets go through the steps on how to build the OAuth2 security and add it to your FastAPI provider.

### Step 1: Initial Setup of FastAPI, FastAPIAdapter, and Workflows
We start by defining the FastAPI app, setting up the AutoGenWorkflows object, and registering a simple workflow (simple_workflow) for the adapter.

```python
    {!> docs_src/user_guide/adapters/fastapi/security/main_1_fastapi.py [ln:14-18]!}
```

`AutoGenWorkflows`: Manages and registers workflows. Here, the simple_workflow is registered under the name "simple_learning".
`FastAPIAdapter`: We'll attach the adapter to the FastAPI app later. It exposes the workflows as REST APIs.

### Step 2: Mock Database Setup
This step sets up a mock database with two users (johndoe and alice). This is a simplified user store for the example, where each user has attributes like username, email, and hashed_password.

```python
    {!> docs_src/user_guide/adapters/fastapi/security/main_1_fastapi.py [ln:25-42]!}
```

`fake_users_db`: A dictionary that represents a mock database of users. Each user has attributes like `hashed_password`, `disabled` (for checking active users), and `user_id` (which we will use for authorization).

### Step 3: OAuth2 Authentication Setup
Here we configure OAuth2 with password flow and token-based authentication. This ensures that users authenticate with a username and password, and the app generates a token.

```python
    {!> docs_src/user_guide/adapters/fastapi/security/main_1_fastapi.py [ln:44-48]!}
```

`OAuth2PasswordBearer`: This is used to handle token-based authentication. `tokenUrl="token"` indicates that users will obtain a token by calling the `/token` endpoint.
`fake_hash_password`: A simple mock function to simulate password hashing.

### Step 4: User Authentication Logic
This step simulates user lookup, token decoding, and user validation. The token received in API requests is decoded to get the user, and the user’s information is validated for authorization.

```python
    {!> docs_src/user_guide/adapters/fastapi/security/main_1_fastapi.py [ln:51-74]!}
```

`User and UserInDB`: These Pydantic models represent user data. UserInDB extends User by adding a hashed_password field for password comparison.
`get_user`: This function retrieves user data from `fake_users_db`.
`fake_decode_token`: Simulates the process of decoding a token to extract user information (in this mock, the token is just the username).

### Step 5: OAuth2 Token Login Endpoint
This step defines the `/token` endpoint where users submit their username and password to receive an authentication token (mocked as the username). The system checks if the password matches before generating the token.

```python
    {!> docs_src/user_guide/adapters/fastapi/security/main_1_fastapi.py [ln:96-106]!}
```

`/token`: This endpoint handles user login. If the username and password match, it returns a token in the form of the username. Otherwise, an error is returned.

### Step 6: Securing Routes with OAuth2
Here we secure the FastAPI routes by requiring the user to pass an OAuth2 token to authenticate and authorize requests.

```python
    {!> docs_src/user_guide/adapters/fastapi/security/main_1_fastapi.py [ln:77-93]!}
```

`get_current_user`: This function extracts the token from the request, decodes it, and returns the user object if valid. If the token is invalid, a 401 error is returned.
`get_current_active_user`: It checks whether the user account is active `(disabled = False)`, raising an error if the user is inactive.

### Step 7: Custom Client ID Generation
This step extracts the user’s user_id from the current authenticated user and provides it to the adapter. This will allow syncing client information during workflow interactions.

```python
    {!> docs_src/user_guide/adapters/fastapi/security/main_1_fastapi.py [ln:114-117]!}
```

`get_user_id`: Returns the user_id of the authenticated user, which is later used for authorization in the workflows.

### Step 8: Connecting the Adapter and Securing It
Finally, we connect the FastAPIAdapter to the FastAPI app. The get_user_id function is passed as a security dependency, ensuring that every internal API call is secured.

```python
    {!> docs_src/user_guide/adapters/fastapi/security/main_1_fastapi.py [ln:119-120]!}
```

`get_user_id`: This function ensures that the `user_id` of the authenticated user is passed with every internal request, securing the workflows exposed by the adapter.

### Step 9: Workflow Listing Endpoint
We add an optional `/` endpoint to list the available workflows, which can be useful for understanding what workflows are currently available in the FastAPIAdapter.

```python
    {!> docs_src/user_guide/adapters/fastapi/security/main_1_fastapi.py [ln:123-125]!}
```

`/`: Lists the available workflows and their descriptions for easier access and understanding of what the API offers.

### Final Explanation
In this setup:

 - Authentication is handled using OAuth2, with token generation via a mock `/token` endpoint.

 - User information is stored in a mock database, and token-based authentication ensures that only valid users can interact with the workflows.

 - The `get_user_id` function is the central security mechanism, ensuring that each user’s actions are tracked and authorized via their `user_id`.

 - By attaching the `get_user_id` function to the FastAPIAdapter, we effectively secure all the internal API calls exposed by the workflows, providing a scalable and consistent approach to authorization and client sync.
