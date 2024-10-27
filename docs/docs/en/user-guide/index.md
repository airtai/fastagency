# Introduction to FastAgency

**FastAgency** is an open-source framework designed to accelerate the transition from prototype to production for multi-agent AI workflows. For developers who use the AutoGen framework, FastAgency enables you to seamlessly scale Jupyter notebook prototypes into fully functional, production-ready applications. With multi-framework support, a unified programming interface, and powerful API integration capabilities, FastAgency streamlines the deployment process, saving time and effort while maintaining flexibility and performance.

Whether you're orchestrating complex AI agents or integrating external APIs into workflows, FastAgency provides the tools necessary to quickly transition from concept to production, reducing development cycles and allowing you to focus on optimizing your multi-agent systems.

## Key Features

- [**Multi-Runtime Support**](runtimes/index.md): FastAgency supports multiple agentic [runtimes](runtimes/index.md) to provide maximum flexibility. Currently, it supports **AutoGen** and plans to extend support to [CrewAI](https://www.crewai.com/){target="_blank"}. This ensures that as the AI ecosystem evolves, FastAgency remains a reliable and adaptable framework, capable of leveraging emerging agentic technologies. Developers can easily switch between frameworks, choosing the best one for their project's specific needs.

- [**Unified Programming Interface Across UIs**](ui/index.md): FastAgency features a **common programming interface** that enables you to develop your core workflows once and reuse them across various user interfaces without rewriting code. This includes support for both **console-based applications** via `ConsoleUI` and **web-based applications** via `MesopUI`. Whether you need a command-line tool or a fully interactive web app, FastAgency allows you to deploy the same underlying workflows across environments, saving development time and ensuring consistency.

- [**Seamless External API Integration**](api/index.md): One of FastAgency's standout features is its ability to easily integrate external APIs into your agent workflows. With just a **single line of code**, you can import an OpenAPI specification, and in only one more line, you can connect it to your agents. This dramatically simplifies the process of enhancing AI agents with real-time data, external processing, or third-party services. For example, you can easily integrate a weather API to provide dynamic, real-time weather updates to your users, making your application more interactive and useful with minimal effort.

- [**Tester Class for Continuous Integration**](testing/index.md): FastAgency also provides a **Tester Class** that enables developers to write and execute tests for their multi-agent workflows. This feature is crucial for maintaining the reliability and robustness of your application, allowing you to automatically verify agent behavior and interactions. The Tester Class is designed to integrate smoothly with **continuous integration (CI)** pipelines, helping you catch bugs early and ensure that your workflows remain functional as they scale into production.

- [**Command-Line Interface (CLI) for Orchestration**](cli/index.md): FastAgency includes a powerful **command-line interface (CLI)** for orchestrating and managing multi-agent applications directly from the terminal. The CLI allows developers to quickly run workflows, pass parameters, and monitor agent interactions without needing a full GUI. This is especially useful for automating deployments and integrating workflows into broader DevOps pipelines, enabling developers to maintain control and flexibility in how they manage AI-driven applications.

## Why FastAgency?

FastAgency bridges the gap between rapid prototyping and production-ready deployment, empowering developers to bring their multi-agent systems to life quickly and efficiently. By integrating familiar frameworks like AutoGen, providing powerful API integration, and offering robust CI testing tools, FastAgency reduces the complexity and overhead typically associated with deploying AI agents in real-world applications.

Whether you’re building interactive console tools, developing fully-featured web apps, or orchestrating large-scale multi-agent systems, FastAgency is built to help you deploy faster, more reliably, and with greater flexibility.

## ⭐⭐⭐ Stay in touch ⭐⭐⭐

Stay up to date with new features and integrations by following our documentation and community updates on our [**Discord server**](https://discord.gg/kJjSGWrknU){target="_blank"}. FastAgency is continually evolving to support new frameworks, APIs, and deployment strategies, ensuring you remain at the forefront of AI-driven development.

Last but not least, show us your support by giving a star to our [**GitHub repository**](https://github.com/airtai/fastagency/){target="_blank"}.
