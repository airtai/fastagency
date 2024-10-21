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

<details>
    <summary>workflows.py</summary>
    ```python
    {!> docs_src/user_guide/adapters/fastapi/security/workflows.py !}
    ```
</details>

You can start this secured adapter using the following command:

```
uvicorn main:app --host 0.0.0.0 --port 8008
```

Now, lets go through the steps on how to build the OAuth2 security and add it to your FastAPI provider.
