> **_NOTE:_**  This is an auto-generated file. Please edit docs/docs/en/contributing/CONTRIBUTING.md instead.

# Development Environment Setup

You can set up the development environment using one of two methods:

1. **Using GitHub Codespaces**
2. **Setting Up Locally with Dev Containers**


## Using GitHub Codespaces

Using GitHub Codespaces is the fastest way to contribute without setting up a local development environment.

Follow the steps below to begin contributing using Codespaces.

### 1. Fork the Repository

- Navigate to the <a href="https://github.com/airtai/fastagency" target="_blank">FastAgency GitHub repository</a>.
- Click on the **Fork** button in the top-right corner to create your own copy of the repository.

### 2. Open a Codespace

- In your forked repository, navigate to the main page.
- Ensure you are on the **main** branch.
- Click the **< > Code** button, then select the **Codespaces** tab.
- Click on **Create codespace on main**.

#### Advanced Options

- If you choose to configure advanced options, you will have the opportunity to set optional environment secrets needed for development while starting the codespace.
- For detailed instructions related to advanced options, refer to the <a href="https://docs.github.com/en/codespaces/developing-in-a-codespace/creating-a-codespace-for-a-repository#creating-a-codespace-for-a-repository" target="_blank">GitHub Codespaces documentation</a>.

> **Note:** If you create the Codespace using the default options, you may not see an option to set environment variables during setup. However, you can set them later in the terminal after starting the Codespace, as needed. For a list of environment variables, please refer to the section [below](#list-of-optional-environment-variables).


#### Setting Environment Variables (Optional)

If you choose to configure advanced options when creating the Codespace, you might see a section called <a href="https://docs.github.com/en/codespaces/developing-in-a-codespace/creating-a-codespace-for-a-repository#recommended-secrets" target="_blank">Recommended secrets</a>. These are optional and depend on the parts of the codebase you plan to work on.

#### Working with External APIs

If your contributions involve interacting with external APIs (e.g., OpenAI), you need to provide your own API keys.

- **For example**, to work with OpenAI services, set the `OPENAI_API_KEY` environment variable.

#### How to Set Environment Variables

- While creating the Codespace, find the section for **Recommended secrets** and enter the necessary keys.
- You can also set the keys as environment variables after starting the Codespace in the terminal.

#### List of Optional environment variables

The table below provides a list of optional environment variables that you may need to set.

| Name                  | Description                                                                                                                                               |
|--------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------|
| `OPENAI_API_KEY`          | Optional; needed if working on OpenAI-related code. Can be set later in the Codespace terminal.                                                           |
| `TOGETHER_API_KEY`        | Optional; needed if working with Together API-related code. Can be set later in the Codespace terminal.                                                   |
| `ANTHROPIC_API_KEY`       | Optional; needed if working with Anthropic API-related code. Can be set later in the Codespace terminal.                                                  |
| `AZURE_OPENAI_API_KEY`    | Optional; required if using Azure's OpenAI services. Also set `AZURE_API_ENDPOINT`, `AZURE_API_VERSION`, and at least one Azure model.                     |
| `AZURE_API_ENDPOINT`      | Required with `AZURE_OPENAI_API_KEY`, `AZURE_API_VERSION`, and at least one Azure model when using Azure's OpenAI services. Can be set later in the Codespace terminal.             |
| `AZURE_API_VERSION`       | Required with `AZURE_OPENAI_API_KEY`, `AZURE_API_ENDPOINT`, and at least one Azure model when using Azure's OpenAI services. Can be set later in the Codespace terminal.                 |
| `AZURE_GPT35_MODEL`       | Required if using Azure's GPT-3.5 model; must also set other Azure-related keys. Can be configured later as an environment variable.                      |
| `AZURE_GPT4_MODEL`        | Required if using Azure's GPT-4 model; must also set other Azure-related keys. Can be configured later in the Codespace terminal.                         |
| `AZURE_GPT4o_MODEL`       | Required if using Azure's GPT-4o model; must also set other Azure-related keys. Can be configured later as an environment variable.                       |
| `BING_API_KEY`            | Optional; used to enhance WebSurfer agent performance with Bing search and data services. Can be set later as an environment variable.                    |


### 3. Wait for Codespace Initialization

- After initiating the Codespace, wait for it to set up. This may take a few minutes.
- The development environment is configured automatically, including the installation of all dependencies.
- **No manual setup is required on your part.**
- Once the Codespace is ready, you can start coding immediately.


## Setting Up Locally with Dev Containers

Our project supports development using Visual Studio Code's **Dev Containers** feature. This allows contributors to set up a consistent development environment inside a Docker container.

Here's how you can use Dev Containers to contribute to our project:

### Prerequisites

Before you begin, make sure you have the following installed:

- **Visual Studio Code**: Download and install the latest version from the <a href="https://code.visualstudio.com/" target="_blank">official website</a>.
- **Dev Containers Extension**: Open Visual Studio Code, go to the Extensions view (`Ctrl+Shift+X` or `Cmd+Shift+X`), search for "**Dev Containers**" by Microsoft, and install it.
- **Docker**: Install Docker Desktop for your operating system from the <a href="https://www.docker.com/products/docker-desktop" target="_blank">official website</a>. Docker is required to build and run the dev container.


### Setting up the project

#### 1. Fork the repository

- Navigate to the <a href="https://github.com/airtai/fastagency" target="_blank">FastAgency GitHub repository</a>.
- Click on the **Fork** button in the top-right corner to create your own copy of the repository.


#### 2. Clone the forked repository

Clone your forked **FastAgency** repository to your local machine:

```bash
git clone https://github.com/<your-username>/fastagency.git
```

Replace `<your-username>` with your GitHub username.

#### 3. Open the project in a dev container

- Open Visual Studio Code.
- Open the cloned repository folder in Visual Studio Code.
- Visual Studio Code automatically detects that this project uses a dev container and prompts you to reopen the project in the container via a prompt at the bottom right corner of the editor. Click on the **Reopen in Container** button in this prompt to display the Command Palette, where you can choose a container configuration file from the list of options.
- Alternatively, you can launch the Command Palette directly by pressing `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (macOS) and select **Dev Containers: Rebuild and Reopen in Container**. This will also prompt you to choose a container configuration file from the list of options.
- Once you select a configuration file, Visual Studio Code will read the container configuration and reopen the project inside the dev container. You can click on the **Show Logs** link in the prompt displayed at the bottom right to see the live logs.
- The development environment is configured automatically, including the installation of all dependencies.
- **No manual setup is required on your part.**
- Once the devcontainer is ready, you can start coding immediately.


#### 4. Set Optional Environment Variables

Depending on your contribution, you may need to set a few optional environment variables. Please refer to the [list of optional environment variables](#list-of-optional-environment-variables) for details.

## Making Changes and Submitting a Pull Request


1.  **Create a New Branch**
	- From your main branch, create a new branch for your changes or new features.

2.  **Make Your Changes**
	- Implement the necessary changes or add new features in your branch.

3.  **Test Your Changes**
	- Ensure your changes work as expected by running the project's tests or manually testing the functionality.

	- To run tests, use:
		```bash
		pytest tests
		```

	- In the project, you'll find some **pytest marks**:
		-  `slow`
		-  `all`

	- By default, running `pytest` will execute tests **not** marked as `slow`.
	- To run all tests, including slow ones, use:
		```bash
		pytest -m 'all'
		```


4.  **Commit and Push Your Changes**
    - After testing, commit your changes to your branch and push them to your forked repository.

5.  **Create a Pull Request**
    - Navigate to your forked repository on GitHub.
    - Create a new pull request targeting our project's main branch.
    - Provide a clear title and description for your changes.

Thank you for your contributions! If you have any questions or need assistance, feel free to <a  href="https://github.com/airtai/fastagency/issues" target="_blank">open an issue</a> or reach out to the maintainers.
