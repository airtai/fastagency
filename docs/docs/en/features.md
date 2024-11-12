---
# 0.5 - API
# 2 - Release
# 3 - Contributing
# 5 - Template Page
# 10 - Default
hide:
  - navigation

search:
  boost: 10
---

<!-- README starts here -->

# FastAgency


<b>The fastest way to bring multi-agent workflows to production.</b>


---

<p align="center">
  <a href="https://github.com/airtai/fastagency/actions/workflows/pipeline.yaml" target="_blank">
    <img src="https://github.com/airtai/fastagency/actions/workflows/pipeline.yaml/badge.svg?branch=main" alt="Test Passing"/>
  </a>

  <a href="https://coverage-badge.samuelcolvin.workers.dev/redirect/airtai/fastagency" target="_blank">
      <img src="https://coverage-badge.samuelcolvin.workers.dev/airtai/fastagency.svg" alt="Coverage">
  </a>

  <a href="https://www.pepy.tech/projects/fastagency" target="_blank">
    <img src="https://static.pepy.tech/personalized-badge/fastagency?period=month&units=international_system&left_color=grey&right_color=green&left_text=downloads/month" alt="Downloads"/>
  </a>

  <a href="https://pypi.org/project/fastagency" target="_blank">
    <img src="https://img.shields.io/pypi/v/fastagency?label=PyPI" alt="Package version">
  </a>

  <a href="https://pypi.org/project/fastagency" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/fastagency.svg" alt="Supported Python versions">
  </a>

  <br/>

  <a href="https://github.com/airtai/fastagency/actions/workflows/codeql.yml" target="_blank">
    <img src="https://github.com/airtai/fastagency/actions/workflows/codeql.yml/badge.svg" alt="CodeQL">
  </a>

  <a href="https://github.com/airtai/fastagency/actions/workflows/dependency-review.yaml" target="_blank">
    <img src="https://github.com/airtai/fastagency/actions/workflows/dependency-review.yaml/badge.svg" alt="Dependency Review">
  </a>

  <a href="https://github.com/airtai/fastagency/blob/main/LICENSE" target="_blank">
    <img src="https://img.shields.io/github/license/airtai/fastagency.png" alt="License">
  </a>

  <a href="https://github.com/airtai/fastagency/blob/main/CODE_OF_CONDUCT.md" target="_blank">
    <img src="https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg" alt="Code of Conduct">
  </a>

  <a href="https://discord.gg/kJjSGWrknU" target="_blank">
      <img alt="Discord" src="https://img.shields.io/discord/1247409549158121512?logo=discord">
  </a>
</p>

---

## What is FastAgency?

For start, FastAgency is not yet another agentic AI framework. There are many such
frameworks available today, the most popular open-source ones being [**AutoGen**](https://github.com/microsoft/autogen){target="_blank"}, [**CrewAI**](https://www.crewai.com/){target="_blank"}, [**Swarm**](https://github.com/openai/swarm){target="_blank"} and [**LangGraph**](https://github.com/langchain-ai/langgraph){target="_blank"}. FastAgency provides you with a unified programming interface for deploying agentic workflows written in above agentic frameworks in both development and productional settings (current version supports [**AutoGen**](https://github.com/microsoft/autogen){target="_blank"} only, but other frameworks will be supported very soon). With only a few lines of code, you can create a web chat application or REST API service interacting with agents of your choice. If you need to scale-up your workloads, FastAgency can help you deploy a fully distributed system using internal message brokers coordinating multiple machines in multiple datacenters with just a few lines of code changed from your local development setup.

**FastAgency** is an open-source framework designed to accelerate the transition from prototype to production for multi-agent AI workflows. For developers who use the AutoGen framework, FastAgency enables you to seamlessly scale Jupyter notebook prototypes into a fully functional, production-ready applications. With multi-framework support, a unified programming interface, and powerful API integration capabilities, FastAgency streamlines the deployment process, saving time and effort while maintaining flexibility and performance.

Whether you're orchestrating complex AI agents or integrating external APIs into workflows, FastAgency provides the tools necessary to quickly transition from concept to production, reducing development cycles and allowing you to focus on optimizing your multi-agent systems.

## Key Features

- [**Multi-Runtime Support**](user-guide/runtimes/index.md): FastAgency supports multiple agentic [runtimes](user-guide/runtimes/index.md) to provide maximum flexibility. Currently, it supports **AutoGen** and plans to extend support to [CrewAI](https://www.crewai.com/){target="_blank"}. This ensures that as the AI ecosystem evolves, FastAgency remains a reliable and adaptable framework, capable of leveraging emerging agentic technologies. Developers can easily switch between frameworks, choosing the best one for their project's specific needs.

- [**Unified Programming Interface Across UIs**](user-guide/ui/index.md): FastAgency features a **common programming interface** that enables you to develop your core workflows once and reuse them across various user interfaces without rewriting code. This includes support for both **console-based applications** via `ConsoleUI` and **web-based applications** via `MesopUI`. Whether you need a command-line tool or a fully interactive web app, FastAgency allows you to deploy the same underlying workflows across environments, saving development time and ensuring consistency.

- [**Seamless External API Integration**](user-guide/api/index.md): One of FastAgency's standout features is its ability to easily integrate external APIs into your agent workflows. With just a **few lines of code**, you can import an OpenAPI specification, and in only one more line, you can connect it to your agents. This dramatically simplifies the process of enhancing AI agents with real-time data, external processing, or third-party services. For example, you can easily integrate a weather API to provide dynamic, real-time weather updates to your users, making your application more interactive and useful with minimal effort.

- [**Tester Class for Continuous Integration**](user-guide/testing/index.md): FastAgency also provides a **Tester Class** that enables developers to write and execute tests for their multi-agent workflows. This feature is crucial for maintaining the reliability and robustness of your application, allowing you to automatically verify agent behavior and interactions. The Tester Class is designed to integrate smoothly with **continuous integration (CI)** pipelines, helping you catch bugs early and ensure that your workflows remain functional as they scale into production.

- [**Command-Line Interface (CLI) for Orchestration**](user-guide/cli/index.md): FastAgency includes a powerful **command-line interface (CLI)** for orchestrating and managing multi-agent applications directly from the terminal. The CLI allows developers to quickly run workflows, pass parameters, and monitor agent interactions without needing a full GUI. This is especially useful for automating deployments and integrating workflows into broader DevOps pipelines, enabling developers to maintain control and flexibility in how they manage AI-driven applications.

## Why FastAgency?

FastAgency bridges the gap between rapid prototyping and production-ready deployment, empowering developers to bring their multi-agent systems to life quickly and efficiently. By integrating familiar frameworks like AutoGen, providing powerful API integration, and offering robust CI testing tools, FastAgency reduces the complexity and overhead typically associated with deploying AI agents in real-world applications.

Whether you’re building interactive console tools, developing fully-featured web apps, or orchestrating large-scale multi-agent systems, FastAgency is built to help you deploy faster, more reliably, and with greater flexibility.

### Supported Runtimes

Currently, the only supported runtime is [**AutoGen**](https://github.com/microsoft/autogen){target="_blank"}, with support for [**CrewAI**](https://www.crewai.com/){target="_blank"}, [**Swarm**](https://github.com/openai/swarm){target="_blank"} and [**LangGraph**](https://github.com/langchain-ai/langgraph){target="_blank"} coming soon.

### Supported User Interfaces

FastAgency currently supports workflows defined using AutoGen and provides options for different types of applications:

- **Console**: Use the [**`ConsoleUI`**](../api/fastagency/ui/console/ConsoleUI.md) interface for command-line based interaction. This is ideal for developing and testing workflows in a text-based environment.

- [**Mesop**](https://google.github.io/mesop/){target="_blank"}: Utilize [**`MesopUI`**](../api/fastagency/ui/mesop/MesopUI.md) for web-based applications. This interface is suitable for creating web applications with a user-friendly interface.

### Supported Network Adapters

FastAgency can use chainable network adapters that can be used to easily create
scalable, production ready architectures for serving your workflows. Currently, we
support the following network adapters:

- [**REST API**](https://en.wikipedia.org/wiki/REST){target="_blank"} via [**FastAPI**](https://fastapi.tiangolo.com/){target="_blank"}: Use the [**`FastAPIAdapter`**](../api/fastagency/adapters/fastapi/FastAPIAdapter.md) to serve your workflow using [**FastAPI**](https://fastapi.tiangolo.com/){target="_blank"} server. This setup allows you to work your workflows in multiple workers and serve them using the highly extensible and stable ASGI server.

- [**NATS.io**](https://nats.io/){target="_blank"} via [**FastStream**](https://github.com/airtai/faststream){target="_blank"}: Utilize the [**`NatsAdapter`**](../api/fastagency/adapters/nats/NatsAdapter.md) to use [**NATS.io MQ**](https://nats.io/){target="_blank"} message broker for highly-scalable, production-ready setup. This interface is suitable for setups in VPN-s or, in combination with the [**`FastAPIAdapter`**](../api/fastagency/adapters/fastapi/FastAPIAdapter.md) to serve public workflows in an authenticated, secure manner.


<!-- README insert example here -->

## Future Plans

We are actively working on expanding FastAgency’s capabilities. In addition to supporting AutoGen, we plan to integrate support for other frameworks, other network provider and other UI frameworks.

---

## ⭐⭐⭐ Stay in touch ⭐⭐⭐

Stay up to date with new features and integrations by following our documentation and community updates on our [**Discord server**](https://discord.gg/kJjSGWrknU){target="_blank"}. FastAgency is continually evolving to support new frameworks, APIs, and deployment strategies, ensuring you remain at the forefront of AI-driven development.

Last but not least, show us your support by giving a star to our [**GitHub repository**](https://github.com/airtai/fastagency/){target="_blank"}.


Your support helps us to stay in touch with you and encourages us to
continue developing and improving the framework. Thank you for your
support!

---

## Contributors

Thanks to all of these amazing people who made the project better!

<a href="https://github.com/airtai/fastagency/graphs/contributors" target="_blank">
  <img src="https://contrib.rocks/image?repo=airtai/fastagency"/>
</a>
