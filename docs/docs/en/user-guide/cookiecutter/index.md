# Project Setup Using Cookiecutter

Cookiecutter creates projects from cookiecutters (project templates), e.g. Python package projects from Python package templates. `FastAgency` provides a [cookiecutter template](https://github.com/airtai/cookiecutter-fastagency) to quickly setup environment and to quickly run the desired example.

### Using Cookiecutter Template

=== "Cookiecutter"

    1. Install Cookiecutter with the following command:
       ```console
       pip install cookiecutter
       ```

    2. Run the `cookiecutter` command:
       ```console
       cookiecutter https://github.com/airtai/cookiecutter-fastagency.git
       ```

    3. Depending on the type of the project, choose the appropriate option in step 3:

        === "Console"
            ```console
            [1/3] project_name (My FastAgency App):
            [2/3] project_slug (my_fastagency_app):
            [3/3] Select app_type
                1 - fastapi+mesop
                2 - mesop
                3 - console
                4 - nats+fastapi+mesop
                Choose from [1/2/3/4] (1): 3
            ```

            This command installs FastAgency with support for the Console interface and the AutoGen framework.

        === "Mesop"
            ```console
            [1/3] project_name (My FastAgency App):
            [2/3] project_slug (my_fastagency_app):
            [3/3] Select app_type
                1 - fastapi+mesop
                2 - mesop
                3 - console
                4 - nats+fastapi+mesop
                Choose from [1/2/3/4] (1): 2
            ```

            This command installs FastAgency with support for both the Console and Mesop interfaces for AutoGen workflows.

        === "FastAPI + Mesop"
            ```console
            [1/3] project_name (My FastAgency App):
            [2/3] project_slug (my_fastagency_app):
            [3/3] Select app_type
                1 - fastapi+mesop
                2 - mesop
                3 - console
                4 - nats+fastapi+mesop
                Choose from [1/2/3/4] (1): 1
            ```

            This command installs FastAgency with support for both the Console and Mesop interfaces for AutoGen workflows, with FastAPI handling input requests and workflow execution.

        === "NATS + FastAPI + Mesop"
            ```console
            [1/3] project_name (My FastAgency App):
            [2/3] project_slug (my_fastagency_app):
            [3/3] Select app_type
                1 - fastapi+mesop
                2 - mesop
                3 - console
                4 - nats+fastapi+mesop
                Choose from [1/2/3/4] (1): 4
            ```

            This command installs FastAgency with support for both the Console and Mesop interfaces for AutoGen workflows, with FastAPI serving input and independent workers communicating over the NATS.io protocol workflows. This is the most scable setup, recommended for large production workloads.

    4. Executing the `cookiecutter` command will create the following file structure:

        === "Console"
            ```console
            my_fastagency_app/
            ├── .devcontainer
            │   ├── devcontainer.env
            │   ├── devcontainer.json
            │   ├── docker-compose.yml
            │   └── setup.sh
            ├── .github
            │   └── workflows
            │       └── test.yml
            ├── LICENSE
            ├── README.md
            ├── my_fastagency_app
            │   ├── __init__.py
            │   ├── main.py
            │   └── workflow.py
            ├── pyproject.toml
            └── tests
                ├── __init__.py
                ├── conftest.py
                └── test_workflow.py
            ```
        === "Mesop"
            ```console
            my_fastagency_app/
            ├── .devcontainer
            │   ├── devcontainer.env
            │   ├── devcontainer.json
            │   ├── docker-compose.yml
            │   └── setup.sh
            ├── .github
            │   └── workflows
            │       └── test.yml
            ├── LICENSE
            ├── README.md
            ├── my_fastagency_app
            │   ├── __init__.py
            │   ├── main.py
            │   └── workflow.py
            ├── pyproject.toml
            └── tests
                ├── __init__.py
                ├── conftest.py
                └── test_workflow.py
            ```
        === "FastAPI + Mesop"
            ```console
            my_fastagency_app/
            ├── .devcontainer
            │   ├── devcontainer.env
            │   ├── devcontainer.json
            │   ├── docker-compose.yml
            │   └── setup.sh
            ├── .github
            │   └── workflows
            │       └── test.yml
            ├── LICENSE
            ├── README.md
            ├── my_fastagency_app
            │   ├── __init__.py
            │   ├── main_1_fastapi.py
            │   ├── main_2_mesop.py
            │   └── workflow.py
            ├── pyproject.toml
            └── tests
                ├── __init__.py
                ├── conftest.py
                └── test_workflow.py
            ```
        === "NATS + FastAPI + Mesop"
            ```console
            my_fastagency_app/
            ├── .devcontainer
            │   ├── devcontainer.env
            │   ├── devcontainer.json
            │   ├── docker-compose.yml
            |   ├── nats_server.conf
            │   └── setup.sh
            ├── .github
            │   └── workflows
            │       └── test.yml
            ├── LICENSE
            ├── README.md
            ├── my_fastagency_app
            │   ├── __init__.py
            │   ├── main_1_nats.py
            │   ├── main_2_fastapi.py
            │   ├── main_3_mesop.py
            │   └── workflow.py
            ├── pyproject.toml
            └── tests
                ├── __init__.py
                ├── conftest.py
                └── test_workflow.py
            ```

    5. To run LLM-based applications, you need an API key for the LLM used. The most commonly used LLM is [OpenAI](https://platform.openai.com/docs/models). To use it, create an [OpenAI API Key](https://openai.com/index/openai-api/) and set it as an environment variable in the terminal using the following command:

        ```console
        export OPENAI_API_KEY=openai_api_key_here
        ```

        If you want to use a different LLM provider, follow [this guide](https://fastagency.ai/latest/user-guide/runtimes/autogen/using_non_openai_models/).

        Alternatively, you can skip this step and set the LLM API key as an environment variable later in the devcontainer's terminal. If you open the project in [Visual Studio Code](https://code.visualstudio.com/){target="_blank"} using GUI, you will need to manually set the environment variable in the devcontainer's terminal.

    6. Open the generated project in [Visual Studio Code](https://code.visualstudio.com/){target="_blank"} with the following command:
        ```console
        code my_fastagency_app
        ```

    7. Once the project is opened, you will get the following option to reopen it in a devcontainer:

        <img src="../../getting-started/images/reopen-in-container.png" width="600" class="center">

    8. After reopening the project in devcontainer, you can verify that the setup is correct by running the provided tests with the following command:

        ```console
        pytest
        ```

        You should get the following output if everything is correctly setup.
        ```console
        =================================== test session starts ===================================
        platform linux -- Python 3.12.7, pytest-8.3.3, pluggy-1.5.0
        rootdir: /workspaces/my_fastagency_app
        configfile: pyproject.toml
        plugins: asyncio-0.24.0, anyio-4.6.2.post1
        asyncio: mode=Mode.STRICT, default_loop_scope=None
        collected 1 item

        tests/test_workflow.py .                                                            [100%]

        ==================================== 1 passed in 1.02s ====================================
        ```