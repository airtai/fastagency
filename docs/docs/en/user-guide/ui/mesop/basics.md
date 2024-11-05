# Mesop

[**`MesopUI`**](../../../../api/fastagency/ui/mesop/MesopUI.md) in FastAgency offers a web-based interface for interacting with [**multi-agent workflows**](https://microsoft.github.io/autogen/0.2/docs/Use-Cases/agent_chat){target="_blank"}. Unlike the [**`ConsoleUI`**](../../../../api/fastagency/ui/console/ConsoleUI.md), which is text-based and runs in the command line, MesopUI provides a user-friendly browser interface, making it ideal for applications that need a more engaging, graphical interaction. MesopUI is perfect for building interactive web applications and enabling users to interact with agents in a more intuitive way.

When creating a Mesop application, you can choose between two modes:

- **Without Authentication**: Open access to all users.
- **With Authentication**: Access restricted to authenticated users, using [**Firebase**](https://firebase.google.com){target="_blank"} as the authentication provider.

!!! note
    Currently, [**Firebase**](https://firebase.google.com){target="_blank"} is the only supported authentication provider, with Google as the available sign-in method. Future releases will introduce more sign-in options within Firebase and expand support for additional authentication providers.

Below, we’ll walk through the steps to set up a basic student-teacher conversation with **[MesopUI](../../../../api/fastagency/ui/mesop/MesopUI.md)**, highlighting the process for adding authentication.

## Prerequisites

=== "Without Authentication"

    No prerequisites are required for this mode

=== "With Authentication"

    To enable Firebase authentication,  follow these steps to set up your Firebase project and configure access:

    1. #### Create a Firebase Account:

        Sign up for a [**Firebase account**](https://firebase.google.com){target="_blank"} and create a new project on the [**Firebase Console**](https://console.firebase.google.com/){target="_blank"}. If you’re unfamiliar with the process, refer to [**this guide on setting up a new Firebase account and project**](https://support.google.com/appsheet/answer/10104995?sjid=6529592038724640288-AP){target="_blank"}.

    2. #### Configure Firebase Project:

        To integrate Firebase with your Mesop application, you’ll need the **Firebase configuration** and **service account credentials**. Follow these steps to retrieve them:

        - **Firebase Configuration**: Retrieve the configuration keys for your web application. Follow this [**guide**](https://support.google.com/firebase/answer/7015592?hl=en#web&zippy=%2Cin-this-article){target="_blank"} if you need help locating the configuration details.


        - **Service Account Credentials**: Download the service account JSON file. Keep this file secure—do not commit it to Git or expose it in public repositories. Refer to this [**guide**](https://firebase.google.com/docs/admin/setup#initialize_the_sdk_in_non-google_environments){target="_blank"} for detailed instructions.

            !!! danger
                The service account JSON file must be kept secure and should never be committed to Git for security purposes. See [**Best practices**](https://cloud.google.com/iam/docs/best-practices-for-managing-service-account-keys){target="_blank"} for managing service account keys.

    3. #### Enable Google as a Sign-In Method:

        - In this example, we’re using Google as the sign-in method. Enable it in the Firebase Console by following these steps:
            - Open the [**Firebase Console**](https://console.firebase.google.com){target="_blank"} and select your project.
            - Go to **Authentication** > **Sign in method**.
            - Click **Add new provider**, select **Google**, and enable it.
            - Click **Save**

    4. #### Set Up Environment Variables:

        To use Firebase securely, store the configuration and credentials as [**environment variables**](https://en.wikipedia.org/wiki/Environment_variable){target="_blank"}. Run the following commands in the terminal where you’ll launch the FastAgency application. These variables are **essential for the application to function correctly**.

        - **Firebase Configuration Env Variables**:

            Replace each placeholder with the corresponding values from your Firebase configuration

            === "Linux/macOS"
                ```bash
                export FIREBASE_API_KEY="<your_firebase_api_key>"
                export FIREBASE_AUTH_DOMAIN="<your_firebase_auth_domain>"
                export FIREBASE_PROJECT_ID="<your_firebase_project_id>"
                export FIREBASE_STORAGE_BUCKET="<your_firebase_storage_bucket>"
                export FIREBASE_MESSAGING_SENDER_ID="<your_firebase_messaging_sender_id>"
                export FIREBASE_APP_ID="<your_firebase_app_id>"
                ```
            === "Windows"
                ```bash
                set FIREBASE_API_KEY="<your_firebase_api_key>"
                set FIREBASE_AUTH_DOMAIN="<your_firebase_auth_domain>"
                set FIREBASE_PROJECT_ID="<your_firebase_project_id>"
                set FIREBASE_STORAGE_BUCKET="<your_firebase_storage_bucket>"
                set FIREBASE_MESSAGING_SENDER_ID="<your_firebase_messaging_sender_id>"
                set FIREBASE_APP_ID="<your_firebase_app_id>"
                ```

        - **Firebase Service Account Key Env Variable**:

            Set the path to the downloaded service account JSON file:

            === "Linux/macOS"
                ```bash
                export GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/serviceAccountKey.json
                ```

            === "Windows"
                ```bash
                set GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/serviceAccountKey.json
                ```

        - **Application Access Env Variable**:

            The `AUTHORIZED_USER_EMAILS` environment variable controls who can access your Mesop application. When a user signs in with their email, the application checks if this email is included in the authorized list. If the signed-in email isn’t on the list, the user will be denied access.

            You can configure access in two ways:

            - **Restricted Access**: Specify a comma-separated list of authorized email addresses. Only these emails will be allowed access:

                === "Linux/macOS"
                    ```bash
                    export AUTHORIZED_USER_EMAILS=me@example.com,you@example.com,them@example.com
                    ```
                === "Windows"
                    ```bash
                    set AUTHORIZED_USER_EMAILS=me@example.com,you@example.com,them@example.com
                    ```

            - **Unrestricted Access**: To allow access for all users, set the variable to `OPEN_ACCESS`:

                === "Linux/macOS"
                    ```bash
                    export AUTHORIZED_USER_EMAILS="OPEN_ACCESS"
                    ```
                === "Windows"
                    ```bash
                    set AUTHORIZED_USER_EMAILS="OPEN_ACCESS"
                    ```

    With these configurations, you’re ready to add Firebase authentication to your Mesop application!

## Installation

To install **FastAgency** with MesopUI support, use the following command:

=== "Without Authentication"

    ```bash
    pip install "fastagency[autogen,mesop]"
    ```

=== "With Authentication"

    ```bash
    pip install "fastagency[autogen,mesop,firebase]"
    ```

This command ensures that the required dependencies for both **AutoGen** and **Mesop** are installed.

Alternatively, you can use [**Cookiecutter**](../../cookiecutter/index.md), which is the preferred method. Cookiecutter creates the project folder structure, default workflow, automatically installs all the necessary requirements, and creates a [devcontainer](https://code.visualstudio.com/docs/devcontainers/containers){target="_blank"} that can be used with [Visual Studio Code](https://code.visualstudio.com/){target="_blank"}.

## Usage

You can simply create Mesop based UI by importing and instantiating the `MesopUI` class with no parameters:

```python
{! docs_src/user_guide/ui/mesop/main_mesop.py [ln:9] !}

ui = MesopUI()
```

However, you might want to add some customisation to the look-and-feel of the user interface or change some security settings as follows:

### Security

You can pass a custom [SecurityPolicy](https://google.github.io/mesop/api/page/#mesop.security.security_policy.SecurityPolicy){target="_blank"} object and specify things such as:

- a list of allowed iframe parents,

- a list of sites you can connect to,

- a list of sites you load scripts from, and

- a flag to disable trusted types.

```python
{! docs_src/user_guide/ui/mesop/main_mesop.py [ln:4] !}

{! docs_src/user_guide/ui/mesop/main_mesop.py [ln:9] !}

{! docs_src/user_guide/ui/mesop/main_mesop.py [ln:60] !}

ui = MesopUI(security_policy=security_policy)
```

Please see the [Mesop documentation](https://google.github.io/mesop/api/page/#mesop.security.security_policy.SecurityPolicy){target="_blank"} for details.

### Modifying styles

All [Styles](https://google.github.io/mesop/api/style/){target="_blank"} used in styling of Mesop components can be passed to the [`MesopUI`](../../../../api/fastagency/ui/mesop/MesopUI.md)constructor and change the default behavior. They are specified in top-level styling class [`MesopHomePageStyles`](../../../../api/fastagency/ui/mesop/styles/MesopHomePageStyles.md).

```python
{! docs_src/user_guide/ui/mesop/main_mesop.py [ln:4] !}

{! docs_src/user_guide/ui/mesop/main_mesop.py [ln:9] !}

{! docs_src/user_guide/ui/mesop/main_mesop.py [ln:62-86] !}

ui = MesopUI(styles=styles)
```

## Example: Student and Teacher Learning Chat

This example shows how to create a simple learning chat where a student agent interacts with a teacher agent. The student asks questions, and the teacher provides responses, simulating a learning environment. The conversation is facilitated through the web interface using **[MesopUI](../../../../api/fastagency/ui/mesop/MesopUI.md)**.

### Step-by-Step Breakdown

#### 1. **Import Required Modules**
We begin by importing the necessary modules from **FastAgency** and **AutoGen**. These imports provide the essential building blocks for creating agents, workflows, and integrating MesopUI.

=== "Without Authentication"

    ```python
    {!> docs_src/user_guide/ui/mesop/main_mesop.py [ln:1-14] !}
    ```

=== "With Authentication"

    ```python
    {!> docs_src/user_guide/ui/mesop/main_mesop_auth.py [ln:1-15] !}
    ```

    - [**`FirebaseAuth`**](../../../../api/fastagency/ui/mesop/firebase_auth/FirebaseAuth.md) and [**`FirebaseConfig`**](../../../../api/fastagency/ui/mesop/firebase_auth/FirebaseConfig.md): These classes enable you to integrate Firebase authentication into your Mesop application.

- **ConversableAgent**: This class allows the creation of agents that can engage in conversational tasks.
- **[FastAgency](../../../../api/fastagency/FastAgency.md)**: The core class responsible for orchestrating workflows and connecting them with UIs.
- **[UI](../../../../api/fastagency/UI.md)** and **[MesopUI](../../../../api/fastagency/ui/mesop/MesopUI.md)**: These classes define the user interface for interaction, with **MesopUI** enabling a web-based interaction.
- **[AutoGenWorkflows](../../../../api/fastagency/runtimes/autogen/AutoGenWorkflows.md)**: Manages the creation and execution of multi-agent workflows.

#### 2. **Configure the Language Model (LLM)**
Next, we configure the language model that powers the agents. In this case, we're using **GPT-4o**, and the API key is retrieved from the environment.

```python
{! docs_src/user_guide/ui/mesop/main_mesop.py [ln:16-24] !}
```

- **Explanation**: The configuration specifies the LLM model and API key used for powering the conversation between agents. The temperature is set to `0.0` to ensure deterministic responses from the agents, making interactions consistent and reliable.

#### 3. **Define the Workflow and Agents**
Here, we define a simple workflow where the **Student Agent** interacts with the **Teacher Agent**. The student asks questions, and the teacher responds as a math teacher. The workflow is registered using **AutoGenWorkflows**.

```python
{! docs_src/user_guide/ui/mesop/main_mesop.py [ln:26-58] !}
```

- **Agent Overview**: The **Student Agent** is configured with a system message, "You are a student willing to learn," and will initiate questions during the interaction. The **Teacher Agent**, on the other hand, is set up as a math teacher and will respond to the student's questions.
- **Workflow Registration**: The workflow is registered under the name `simple_learning`. The **ConversableAgent** class is used to represent both the student and teacher agents, allowing them to communicate with each other up to 5 turns before summarizing the conversation using the `reflection_with_llm` method.

#### 4. **Using MesopUI**
Finally, we instantiate **[MesopUI](../../../../api/fastagency/ui/mesop/MesopUI.md)** to link the workflow to a web-based interface. This allows the user to interact with the agents through a web browser.

=== "Without Authentication"
    ```python
    {!> docs_src/user_guide/ui/mesop/main_mesop.py [ln:59-90] !}
    ```

    - **Explanation**: Here, we set up the **MesopUI** as the user interface for the workflow, which will allow the entire agent interaction to take place through a web-based platform.

=== "With Authentication"
    ```python hl_lines="29-36 39-42 44"
    {!> docs_src/user_guide/ui/mesop/main_mesop_auth.py [ln:60-107] !}
    ```

    - **Create Firebase Configuration**: Initiate the [**`FirebaseConfig`**](../../../../api/fastagency/ui/mesop/firebase_auth/FirebaseConfig.md) instance with Firebase-specific settings, like api_key, auth_domain, project_id, etc., make sure to set the necessary environment cariables as mentioned [**here**](#set-up-environment-variables). These settings establish a secure connection between your application and Firebase.

    - **Initialize Firebase Authentication**: Instiantiate the [**`FirebaseAuth`**](../../../../api/fastagency/ui/mesop/firebase_auth/FirebaseAuth.md) with the chosen sign-in method and the Firebase configuration created in the previous step. This setup allows the application to handle user authentication via Google sign-in.

    - **Configure the Mesop UI**: MesopUI is set up with a `security_policy`, `custom` styles, and the `auth` configuration. This step ensures that the user interface for the Mesop application is protected by the specified authentication method.


### Complete Application Code

=== "Without Authentication"

    <details>
        <summary>main.py</summary>
        ```python
        {!> docs_src/user_guide/ui/mesop/main_mesop.py !}
        ```
    </details>

=== "With Authentication"

    <details>
        <summary>main.py</summary>
        ```python
        {!> docs_src/user_guide/ui/mesop/main_mesop_auth.py !}
        ```
    </details>


### Running the Application

The preferred way to run the [**Mesop**](https://google.github.io/mesop/){target="_blank"} application is using a Python WSGI HTTP server like [**Gunicorn**](https://gunicorn.org/){target="_blank"} on Linux and Mac or [**Waitress**](https://docs.pylonsproject.org/projects/waitress/en/stable/){target="_blank"} on Windows.

=== "Cookiecutter"
    !!! note "Terminal"
        ```console
        gunicorn main:app
        ```
=== "env + pip"

    First, install the package using package manager such as `pip` and then run it:

    === "Linux/MacOS"
        !!! note "Terminal"
            ```console
            pip install gunicorn
            gunicorn main:app
            ```

    === "Windows"
        !!! note "Terminal"
            ```console
            pip install waitress
            waitress-serve --listen=0.0.0.0:8000 main:app
            ```

---

!!! note
    Ensure that your OpenAI API key is set in the environment, as the agents rely on it to interact using **gpt-4o-mini**. If the API key is not correctly configured, the application may fail to retrieve LLM-powered responses.

### Output

The outputs will vary based on the interface, here is the output of the last terminal starting UI:

```console
[2024-10-15 16:57:44 +0530] [36365] [INFO] Starting gunicorn 23.0.0
[2024-10-15 16:57:44 +0530] [36365] [INFO] Listening at: http://127.0.0.1:8000 (36365)
[2024-10-15 16:57:44 +0530] [36365] [INFO] Using worker: sync
[2024-10-15 16:57:44 +0530] [36366] [INFO] Booting worker with pid: 36366
```
=== "Without Authentication"

    ![Initial message](../../../getting-started/images/chat.png)

=== "With Authentication"

    ![Initial message](./images/auth_login.png)
    ![Initial message](./images/auth_chat.png)

## Debugging Tips
If you encounter issues running the application, ensure that:

- The OpenAI API key is correctly set in your environment variables.
- All necessary packages are installed, especially the `fastagency[autogen,mesop]` dependencies.
- The MesopUI web interface is accessible from the browser, and no firewall is blocking the connection.

---

By using **[MesopUI](../../../../api/fastagency/ui/mesop/MesopUI.md)**, developers can create interactive, web-based multi-agent applications with ease. This interface is ideal for building user-friendly, browser-accessible systems, enabling users to interact with agents in a more engaging and visual environment. You can extend this workflow for more complex scenarios, such as tutoring systems, customer support, or real-time information retrieval.
