## Project setup

We **strongly recommend** using [**Cookiecutter**](../../user-guide/cookiecutter/index.md) for setting up the project. It creates the project folder structure, default workflow, automatically installs all the necessary requirements, and creates a [devcontainer](https://code.visualstudio.com/docs/devcontainers/containers){target="_blank"} that can be used with [Visual Studio Code](https://code.visualstudio.com/){target="_blank"} for development.

You could also use virtual environment managers such as [venv](https://docs.python.org/3/library/venv.html){target="_blank"}, and a Python package manager, such as [pip](https://en.wikipedia.org/wiki/Pip_(package_manager)).


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

        ```console
        [1/4] project_name (My FastAgency App):
        [2/4] project_slug (my_fastagency_app):
        [3/4] Select app_type
            1 - fastapi+mesop
            2 - mesop
            3 - nats+fastapi+mesop
            Choose from [1/2/3] (1): 2
        [4/4] Select python_version
            1 - 3.12
            2 - 3.11
            3 - 3.10
            Choose from [1/2/3] (1):
        ```

        This command installs FastAgency with support for both the Console and Mesop interfaces for AG2 workflows.


    4. Executing the `cookiecutter` command will create the following file structure:

        ```console
        {!> docs_src/getting_started/no_auth/mesop/folder_structure.txt !}
        ```

    5. To run LLM-based applications, you need an API key for the LLM used. The most commonly used LLM is [OpenAI](https://platform.openai.com/docs/models). To use it, create an [OpenAI API Key](https://openai.com/index/openai-api/) and set it as an environment variable in the terminal using the following command:

        ```console
        export OPENAI_API_KEY=openai_api_key_here
        ```

        If you want to use a different LLM provider, follow [this guide](https://fastagency.ai/latest/user-guide/runtimes/ag2/using_non_openai_models/).

        Alternatively, you can skip this step and set the LLM API key as an environment variable later in the devcontainer's terminal. If you open the project in [Visual Studio Code](https://code.visualstudio.com/){target="_blank"} using GUI, you will need to manually set the environment variable in the devcontainer's terminal.

    6. Open the generated project in [Visual Studio Code](https://code.visualstudio.com/){target="_blank"} with the following command:
        ```console
        code my_fastagency_app
        ```

    7. Once the project is opened, you will get the following option to reopen it in a devcontainer:

        <img src="../../user-guide/getting-started/images/reopen-in-container.png" width="600" class="center">

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


    9. Install additional dependencies which will be needed for this tutorial:
        ```bash
        pip install "fastagency[openapi]"
        ```


    !!! info
        If you used a different `project_slug` than the default `my_fastagency_app` this will be reflected in the project module naming. Keep this in mind when running the commands further in this guide (in [Run Application](#running-the-application)), you will need to replace `my_fastagency_app` with your `project_slug` name.


=== "env + pip"

    To get started, you need to install FastAgency with OpenAPI submodule. You can do this using `pip`, Python's package installer.

    ```bash
    pip install "fastagency[autogen,mesop,openapi]"
    ```

## Workflow Code
You need to define the workflow that your application will use. This is where you specify how the agents interact and what they do.
=== "Cookiecutter"
    Workflow will be generated within the `my_fastagency_app/workflow.py` folder. You will need to replace the existing `workflow.py` with the code below.
=== "env + pip"
    Create `workflow.py` and paste the code below inside.


## Deployment Code
=== "Cookiecutter"
    Deployment files will be generated under `my_fastagency_app/deployment` folder. Generated `main.py` should be the same as the code below. You don't need change anything.
=== "env + pip"
    Create `deployment/main.py` and paste the code below inside.

<details>
<summary>main.py</summary>
```python
{! docs_src/getting_started/no_auth/mesop/my_fastagency_app/my_fastagency_app/deployment/main.py [ln:1-10] !}
```

</details>


## Starting the Application

The FastAgency app is created, using the registered workflows (**`wf`**) and web-based user interface ([**`MesopUI`**](../../api/fastagency/ui/mesop/MesopUI.md)). This makes the conversation between agents and the user interactive.

```python
{! docs_src/getting_started/no_auth/mesop/my_fastagency_app/my_fastagency_app/deployment/main.py [ln:6-10] !}
```

For more information, visit [**Mesop User Guide**](../../user-guide/ui/mesop/basics.md){target="_blank"}.


## Running the Application

The preferred way to run the [**Mesop**](https://google.github.io/mesop/){target="_blank"} application is using a Python WSGI HTTP server like [**Gunicorn**](https://gunicorn.org/){target="_blank"} on Linux and Mac or [**Waitress**](https://docs.pylonsproject.org/projects/waitress/en/stable/){target="_blank"} on Windows.

=== "Cookiecutter"
    !!! note "Terminal"
        ```console
        gunicorn my_fastagency_app.deployment.main:app
        ```
=== "env + pip"

    First, install the package using package manager such as `pip` and then run it:

    === "Linux/MacOS"
        !!! note "Terminal"
            ```console
            pip install gunicorn
            gunicorn deployment.main:app
            ```

    === "Windows"
        !!! note "Terminal"
            ```console
            pip install waitress
            waitress-serve --listen=0.0.0.0:8000 deployment.main:app
            ```

```console
[2024-10-10 13:19:18 +0530] [23635] [INFO] Starting gunicorn 23.0.0
[2024-10-10 13:19:18 +0530] [23635] [INFO] Listening at: http://127.0.0.1:8000 (23635)
[2024-10-10 13:19:18 +0530] [23635] [INFO] Using worker: sync
[2024-10-10 13:19:18 +0530] [23645] [INFO] Booting worker with pid: 23645
```

The command will launch a web interface where users can input their requests and interact with the agents (in this case ***http://localhost:8000***)

!!! note
    Ensure that your OpenAI API key is set in the environment, as the agents rely on it to interact using GPT-4o. If the API key is not correctly configured, the application may fail to retrieve LLM-powered responses.
