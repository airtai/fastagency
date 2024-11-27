# API Integration

FastAgency makes it easy to integrate external APIs into your multi-agent workflows, allowing agents to access and interact with real-time data. By leveraging FastAgency's API support, developers can automatically create functions properly annotated for use with large language models (LLMs). This functionality allows agents to fetch and process external information seamlessly.

Currently, FastAgency supports importing API functionality from [**OpenAPI**](https://swagger.io/specification/) specifications, enabling developers to connect their agents with RESTful APIs effortlessly. In addition, we support various types of security for accessing APIs, ensuring your integrations are both functional and secure.

## API Features in FastAgency

### 1. **[Code Injection](./code_injection/index.md)**
FastAgency offers a secure way to manage sensitive data using code injection. With the [**`inject_params`**](../../api/fastagency/api/code_injection/inject_params.md) function, sensitive information, such as tokens, is injected directly into functions without being exposed to the LLM. This ensures that sensitive data remains private while allowing agents to perform the required tasks. The process helps maintain data security and confidentiality while still enabling the proper execution of functions within the workflow.

[Learn more about Code Injection →](./code_injection/index.md)


### 2. **[OpenAPI Import](./openapi/index.md)**
FastAgency can automatically generate API functions from OpenAPI specifications, streamlining the process of connecting agents to external services. With just a few lines of code, you can import an API specification, and FastAgency will handle the function generation and LLM integration, making it simple for agents to call external APIs.

[Learn more about OpenAPI Import →](./openapi/index.md)

### 3. **[API Security](./security.md)**
FastAgency supports different types of security for REST APIs, including OAuth, API keys, and more. This ensures that your API integrations are secure and can handle sensitive data. Our API security mechanisms are flexible, allowing you to configure and manage secure communication between your agents and external APIs.

[Learn more about API Security →](./security.md)

---

FastAgency’s API integration capabilities allow your multi-agent systems to interact with the real world in meaningful ways. Whether you’re pulling data from an external service or managing secure connections, FastAgency provides the tools you need to build powerful, connected applications.

For more updates and discussions, join our [**Discord channel**](https://discord.gg/kJjSGWrknU).
