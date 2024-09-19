---
# 0.5 - API
# 2 - Release
# 3 - Contributing
# 5 - Template Page
# 10 - Default
search:
  boost: 3
---

# Development Environment Setup

You can set up the development environment using one of two methods:

1. **Using GitHub Codespaces**
2. **Cloning the Repository**

---

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

- If you choose to configure advanced options, you will have the opportunity to set optional environment secrets needed for development.
- For detailed instructions related to advanced options, refer to the <a href="https://docs.github.com/en/codespaces/developing-in-a-codespace/creating-a-codespace-for-a-repository#creating-a-codespace-for-a-repository" target="_blank">GitHub Codespaces documentation</a>.

> **Note:** If you create the Codespace using the default options, you might not see the option to set environment variables during setup. In this case, please refer to our [Environment Variables Guide](link_to_environment_variables_guide) for instructions on setting them after creation.

---

### 3. Configure Environment Variables (Optional)

If you choose to configure advanced options when creating the Codespace, you might see a section called [Recommended secrets](https://docs.github.com/en/codespaces/developing-in-a-codespace/creating-a-codespace-for-a-repository#recommended-secrets). These are optional and depend on the parts of the codebase you plan to work on.

#### Working with External APIs

If your contributions involve interacting with external APIs (e.g., OpenAI), you need to provide your own API keys.

- **For example**, to work with OpenAI services, set the `OPENAI_API_KEY` environment variable.

#### How to Set Environment Variables

- While creating the Codespace, find the section for **Recommended secrets** and enter the necessary keys.
- You can also set the keys as environment variables after starting the Codespace in the terminal.

#### List of Required API Keys

- For a comprehensive list of environment variables and API keys, please refer to our [Environment Variables Guide](link_to_environment_variables_guide).

---

### 4. Wait for Codespace Initialization

- After initiating the Codespace, wait for it to set up. This may take a few minutes.
- The development environment is configured automatically, including the installation of all dependencies.
- **No manual setup is required on your part.**

### 5. Start Developing

- Once the Codespace is ready, you can start coding immediately.
- The environment comes with all the tools you need, such as a code editor and terminal access.

### 6. Testing Your Changes

- Run tests directly in the Codespace terminal if needed.
- Use the provided scripts or commands as outlined in the project's documentation.

### 7. Committing Changes

- After making changes, commit them using Git commands within the Codespace.
- Push your commits to your forked repository.

---

## Cloning the Repository

Follow the steps below to set up the development environment locally.

### 1. Clone the Repository

Clone the FastAgency repository to your local machine:

```bash
git clone https://github.com/airtai/fastagency.git
```

### 2: Set Up a Virtual Environment with venv

Create a virtual environment using Python's venv module:

```bash
python -m venv venv
```

This command creates a ./venv/ directory containing Python binaries, allowing you to install packages in an isolated environment.

### 3: Activate the Virtual Environment

Activate the new environment:

```bash
source ./venv/bin/activate
```

Ensure you have the latest pip version in your virtual environment:

```bash
python -m pip install --upgrade pip
```

### 4: Installing Dependencies

After activating the virtual environment as described above, run:

```bash
pip install -e ".[dev]"
```

This will install all the dependencies and your local **FastAgency** in your virtual environment.

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
