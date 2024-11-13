# Project Setup Using Cookiecutter

Cookiecutter creates projects from cookiecutters (project templates), e.g. Python package projects from Python package templates. `FastAgency` provides a [cookiecutter template](https://github.com/airtai/cookiecutter-fastagency) to quickly setup environment and to quickly run the desired example.

### Using Cookiecutter Template

1. Install Cookiecutter with the following command:
    ```console
    pip install cookiecutter
    ```

2. Run the `cookiecutter` command:
    ```console
    cookiecutter https://github.com/airtai/cookiecutter-fastagency.git
    ```

3. Depending on the type of the project, choose the appropriate option in step 3:

    === "Mesop"
        ```console
        [1/5] project_name (My FastAgency App):
        [2/5] project_slug (my_fastagency_app):
        [3/5] Select app_type
            1 - fastapi+mesop
            2 - mesop
            3 - nats+fastapi+mesop
            Choose from [1/2/3] (1): 2
        [4/5] Select python_version
            1 - 3.12
            2 - 3.11
            3 - 3.10
            Choose from [1/2/3] (1):
        [5/5] Select authentication
            1 - basic
            2 - google
            3 - none
            Choose from [1/2/3] (1):
        ```

        This command installs FastAgency with support for both the Console and Mesop interfaces for AutoGen workflows.

    === "FastAPI + Mesop"
        ```console
        [1/5] project_name (My FastAgency App):
        [2/5] project_slug (my_fastagency_app):
        [3/5] Select app_type
            1 - fastapi+mesop
            2 - mesop
            3 - nats+fastapi+mesop
            Choose from [1/2/3] (1): 1
        [4/5] Select python_version
            1 - 3.12
            2 - 3.11
            3 - 3.10
            Choose from [1/2/3] (1):
        [5/5] Select authentication
            1 - basic
            2 - google
            3 - none
            Choose from [1/2/3] (1):
        ```

        This command installs FastAgency with support for both the Console and Mesop interfaces for AutoGen workflows, with FastAPI handling input requests and workflow execution.

    === "NATS + FastAPI + Mesop"
        ```console
        [1/5] project_name (My FastAgency App):
        [2/5] project_slug (my_fastagency_app):
        [3/5] Select app_type
            1 - fastapi+mesop
            2 - mesop
            3 - nats+fastapi+mesop
            Choose from [1/2/3] (1): 3
        [4/5] Select python_version
            1 - 3.12
            2 - 3.11
            3 - 3.10
            Choose from [1/2/3] (1):
        [5/5] Select authentication
            1 - basic
            2 - google
            3 - none
            Choose from [1/2/3] (1):
        ```

        This command installs FastAgency with support for both the Console and Mesop interfaces for AutoGen workflows, with FastAPI serving input and independent workers communicating over the NATS.io protocol workflows. This is the most scable setup, recommended for large production workloads.

4. Executing the `cookiecutter` command will create the following file structure:

    === "Mesop"
        ```console
        {!> docs_src/getting_started/no_auth/mesop/folder_structure.txt !}
        ```
    === "FastAPI + Mesop"
        ```console
        {!> docs_src/getting_started/no_auth/fastapi/folder_structure.txt !}
        ```
    === "NATS + FastAPI + Mesop"
        ```console
        {!> docs_src/getting_started/no_auth/nats_n_fastapi/folder_structure.txt !}
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

    <img src="../getting-started/images/reopen-in-container.png" width="600" class="center">

8. After reopening the project in devcontainer, you can verify that the setup is correct by running the provided tests with the following command:

    ```console
    pytest -s
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

    Running the test could take up to 30 seconds, depending on latency and throughput of OpenAI (or other LLM providers).
