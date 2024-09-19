> **_NOTE:_**  This is an auto-generated file. Please edit docs/docs/en/contributing/CONTRIBUTING.md instead.

# Development Environment Setup

You can set up the development environment using one of two methods:

1. **Using GitHub Codespaces**
2. **Setting Up Locally**


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

- The table below provides a list of optional environment variables that you may need to set.

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


## Setting Up Locally

Follow the steps below to set up the development environment locally.

### 1. Fork the Repository

- Navigate to the <a href="https://github.com/airtai/fastagency" target="_blank">FastAgency GitHub repository</a>.
- Click on the **Fork** button in the top-right corner to create your own copy of the repository.


### 2. Clone the Repository

Clone your forked FastAgency repository to your local machine:

```bash
git clone https://github.com/airtai/fastagency.git
```

### 3. Set Up a Virtual Environment with venv

Create a virtual environment using Python's venv module:

```bash
python -m venv venv
```

This command creates a ./venv/ directory containing Python binaries, allowing you to install packages in an isolated environment.

### 4. Activate the Virtual Environment

Activate the new environment:

```bash
source ./venv/bin/activate
```

Ensure you have the latest pip version in your virtual environment:

```bash
python -m pip install --upgrade pip
```

### 5. Installing Dependencies

After activating the virtual environment as described above, run:

```bash
pip install -e ".[dev]"
```

This will install all the dependencies and your local **FastAgency** in your virtual environment.

### 6. Setting optional environment variables:

Depending on your contribution, you may need to set a few optional environment variables. Please refer to the [list of optional environment variables](#list-of-optional-environment-variables) for details.

## Using Your local **FastAgency**

If you create a Python file that imports and uses **FastAgency**, and run it with the Python from your local environment, it will use your local **FastAgency** source code.

Whenever you update your local **FastAgency** source code, it will automatically use the latest version when you run your Python file again. This is because it is installed with `-e`.

This way, you don't have to "install" your local version to be able to test every change.

## Running Tests

### Pytest

To run tests with your current **FastAgency** application and Python environment, use:

```bash
pytest tests
# or
./scripts/test.sh
# with coverage output
./scripts/test-cov.sh
```

In your project, you'll find some *pytest marks*:

* **slow**
* **all**

By default, running *pytest* will execute "not slow" tests.

To run all tests use:

```bash
pytest -m 'all'
```
