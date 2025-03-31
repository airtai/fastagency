# Mesop

[**`MesopUI`**](../../../../api/fastagency/ui/mesop/MesopUI.md) in FastAgency offers a web-based interface for interacting with [**multi-agent workflows**](https://docs.ag2.ai/docs/user-guide/basic-concepts/orchestration/orchestrations){target="_blank"}. Unlike the [**`ConsoleUI`**](../../../../api/fastagency/ui/console/ConsoleUI.md), which is text-based and runs in the command line, MesopUI provides a user-friendly browser interface, making it ideal for applications that need a more engaging and rich user experience.

When creating a [**Mesop**](https://google.github.io/mesop/){target="_blank"} application, you can choose between the following modes:

- **No Authentication**: Open access to all users.
- **Basic Authentication**: Simple username and password authentication for rapid prototyping. Not recommended for production.
- **Firebase Authentication**: A more robust authentication mechanism that uses [**Firebase**](https://firebase.google.com){target="_blank"} as the provider for authenticating users.

    !!! note
        Currently, [**Firebase**](https://firebase.google.com){target="_blank"} authentication supports only Google as sign-in method. Future releases will introduce more sign-in options within Firebase.

Below, we’ll walk through the steps to set up a basic student-teacher conversation with **[MesopUI](../../../../api/fastagency/ui/mesop/MesopUI.md)**, highlighting the process for adding authentication.

## Prerequisites

=== "No Authentication"

    No prerequisites are required for this mode

=== "Basic Authentication"

    No prerequisites are required for this mode

=== "Firebase Authentication"

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

    4. #### Set Up Environment Variable:

        To securely integrate Firebase, you only need to set one [**environment variable**](https://en.wikipedia.org/wiki/Environment_variable){target="_blank"}, which points to the path of your Firebase service account credentials JSON file. This variable is essential for your FastAgency application to function correctly.

        #### Firebase Service Account Key Env Variable:

        Set the path to your downloaded service account JSON file by running the following command in the terminal where you’ll launch the FastAgency application:

        === "Linux/macOS"
            ```bash
            export GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/serviceAccountKey.json
            ```

        === "Windows"
            ```bash
            set GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/serviceAccountKey.json
            ```

        !!! danger
            The service account JSON file must be kept secure and should never be committed to Git for security purposes. See [**Best practices**](https://cloud.google.com/iam/docs/best-practices-for-managing-service-account-keys){target="_blank"} for managing service account keys.

    With these configurations, you’re ready to add Firebase authentication to your Mesop application!

## Installation

We **strongly recommend** using [**Cookiecutter**](../../../user-guide/cookiecutter/index.md) for setting up the project. Cookiecutter creates the project folder structure, default workflow, automatically installs all the necessary requirements, and creates a [devcontainer](https://code.visualstudio.com/docs/devcontainers/containers){target="_blank"} that can be used with [Visual Studio Code](https://code.visualstudio.com/){target="_blank"}.

You can setup the project using Cookiecutter by following the [**project setup guide**](../../../user-guide/cookiecutter/index.md).

Alternatively, you can use **pip + venv**. To install **FastAgency** with MesopUI support, use the following command:

=== "No Authentication"

    ```bash
    pip install "fastagency[autogen,mesop]"
    ```

=== "Basic Authentication"

    ```bash
    pip install "fastagency[autogen,mesop,basic_auth]"
    ```

=== "Firebase Authentication"

    ```bash
    pip install "fastagency[autogen,mesop,firebase]"
    ```

This command ensures that the required dependencies for both **AG2** and **Mesop** are installed.

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

=== "No Authentication"

=== "Basic Authentication"

=== "Firebase Authentication"

    !!! info
        To support [Firebase's JavaScript libraries](https://firebase.google.com/docs/web/learn-more){target="_blank"}, FastAgency internally adjusts its security policy to allow required resources. Here are the specific adjustments made:

        - **Loosening Trusted Types**:
            `dangerously_disable_trusted_types=True` is enabled. This setting relaxes certain restrictions on JavaScript code execution, allowing Firebase's libraries to function properly.

        - **Allowing Connections to Firebase Resources**:
            The `allowed_connect_srcs` setting is updated to include `*.googleapis.com`, which permits API calls to Firebase and related Google services.

        - **Permitting Firebase Script Sources**:
            The `allowed_script_srcs` setting is modified to allow scripts from `*.google.com`, `https://www.gstatic.com`, `https://cdn.jsdelivr.net`

        These adjustments ensure that Firebase scripts and services can load without conflicts.

For more details on configuring security, see the official [Mesop documentation](https://google.github.io/mesop/api/page/#mesop.security.security_policy.SecurityPolicy){target="_blank"}.

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
We begin by importing the necessary modules from **FastAgency** and **AG2**. These imports provide the essential building blocks for creating agents, workflows, and integrating MesopUI.

=== "No Authentication"

    ```python
    {!> docs_src/user_guide/ui/mesop/main_mesop.py [ln:1-14] !}
    ```

=== "Basic Authentication"

    ```python
    {!> docs_src/user_guide/ui/mesop/main_mesop_basic_auth.py [ln:1-15] !}
    ```

    - [**`BasicAuth`**](../../../../api/fastagency/ui/mesop/auth/basic_auth/BasicAuth.md): This class
    enables you to integrate basic username/password authentication into your Mesop application.

=== "Firebase Authentication"

    ```python
    {!> docs_src/user_guide/ui/mesop/main_mesop_firebase_auth.py [ln:1-15] !}
    ```

    - [**`FirebaseAuth`**](../../../../api/fastagency/ui/mesop/auth/firebase/FirebaseAuth.md) and [**`FirebaseConfig`**](../../../../api/fastagency/ui/mesop/auth/firebase/FirebaseConfig.md): These classes enable you to integrate Firebase authentication into your Mesop application.

- **ConversableAgent**: This class allows the creation of agents that can engage in conversational tasks.
- **[FastAgency](../../../../api/fastagency/FastAgency.md)**: The core class responsible for orchestrating workflows and connecting them with UIs.
- **[UI](../../../../api/fastagency/UI.md)** and **[MesopUI](../../../../api/fastagency/ui/mesop/MesopUI.md)**: These classes define the user interface for interaction, with **MesopUI** enabling a web-based interaction.
- **[Workflow](../../../../api/fastagency/runtimes/ag2/Workflow.md)**: Manages the creation and execution of multi-agent workflows.

#### 2. **Configure the Language Model (LLM)**
Next, we configure the language model that powers the agents. In this case, we're using **GPT-4o**, and the API key is retrieved from the environment.

```python
{! docs_src/user_guide/ui/mesop/main_mesop.py [ln:16-24] !}
```

- **Explanation**: The configuration specifies the LLM model and API key used for powering the conversation between agents. The temperature is set to `0.0` to ensure deterministic responses from the agents, making interactions consistent and reliable.

#### 3. **Define the Workflow and Agents**
Here, we define a simple workflow where the **Student Agent** interacts with the **Teacher Agent**. The student asks questions, and the teacher responds as a math teacher. The workflow is registered using **Workflow**.

```python
{! docs_src/user_guide/ui/mesop/main_mesop.py [ln:26-58] !}
```

- **Agent Overview**: The **Student Agent** is configured with a system message, "You are a student willing to learn," and will initiate questions during the interaction. The **Teacher Agent**, on the other hand, is set up as a math teacher and will respond to the student's questions.
- **Workflow Registration**: The workflow is registered under the name `simple_learning`. The **ConversableAgent** class is used to represent both the student and teacher agents, allowing them to communicate with each other up to 5 turns before summarizing the conversation using the `reflection_with_llm` method.

#### 4. **Using MesopUI**
Finally, we instantiate **[MesopUI](../../../../api/fastagency/ui/mesop/MesopUI.md)** to link the workflow to a web-based interface. This allows the user to interact with the agents through a web browser.

=== "No Authentication"
    ```python
    {!> docs_src/user_guide/ui/mesop/main_mesop.py [ln:59-90] !}
    ```

    - **Explanation**: Here, we set up the **MesopUI** as the user interface for the workflow, which will allow the entire agent interaction to take place through a web-based platform.

=== "Basic Authentication"
    ```python hl_lines="29-37 39"
    {!> docs_src/user_guide/ui/mesop/main_mesop_basic_auth.py [ln:61-101] !}
    ```

    The [**`BasicAuth`**](../../../../api/fastagency/ui/mesop/auth/basic_auth/BasicAuth.md) class allows you to define a set of allowed users with [**bcrypt-hashed**](https://en.wikipedia.org/wiki/Bcrypt){target="_blank"} passwords, providing secure access to your Mesop application. Only users listed in the **`allowed_users`** dictionary can successfully authenticate.

    !!! note

        Only the [**bcrypt**](https://en.wikipedia.org/wiki/Bcrypt){target="_blank"} algorithm is supported for password hashing. Other algorithms, like **MD5** or **SHA-256**, won’t work with this [**`BasicAuth`**](../../../../api/fastagency/ui/mesop/auth/basic_auth/BasicAuth.md) class. Ensure all passwords are hashed using bcrypt.

    **BasicAuth Configuration:**

    1. User Setup:

        - The **`allowed_users`** parameter accepts a dictionary that maps usernames to their [**bcrypt-hashed**](https://en.wikipedia.org/wiki/Bcrypt){target="_blank"} passwords.
        - Only bcrypt hashing is supported; other hashing algorithms (like MD5 or SHA-256) will not work with [**`BasicAuth`**](../../../../api/fastagency/ui/mesop/auth/basic_auth/BasicAuth.md) class.

    2. Hashing Passwords with Bcrypt:

        - For each user, generate a bcrypt hash of their password using tools like the [**Bcrypt Hash Generator**](https://bcrypt.online){target="_blank"}.

    **Generating Bcrypt-Hashed Passwords**

    To quickly create a bcrypt hash for a password, follow these steps:

    1. Open the [**Bcrypt Hash Generator**](https://bcrypt.online){target="_blank"}.
    2. In the `Plain Text Input` field, enter the password `(e.g., someStrongPassword)`.
    3. Set the `Cost Factor` to `10` (default).
    4. Click `GENERATE HASH`.
    5. Copy the hash, which will start with `$2y$...`, and use it as the password for the corresponding user.

    For Example:

    ```py
    allowed_users = {
        "harish": "$2y$10$4aH/.C.WritjZAYskA0Dq.htlFDJTa49UuxSVUlp9JCa2K3PgUkaG"  # nosemgrep
    }
    ```

    In this example, the hash is generated from `someStrongPassword` for the user `harish`.

    **Authenticating in the Mesop Web App**

    To log in, users should enter their **original passwords** (e.g., `someStrongPassword` for  `harish`) on the Mesop application’s login screen. The `BasicAuth` class then verifies the password by comparing its bcrypt hash with the stored hash in `allowed_users`. If the hashes match, the user is successfully authenticated.

=== "Firebase Authentication"
    ```python hl_lines="29-36 39-44 46"
    {!> docs_src/user_guide/ui/mesop/main_mesop_firebase_auth.py [ln:60-107] !}
    ```

    - **Create Firebase Configuration**:

        Initialize the [**`FirebaseConfig`**](../../../../api/fastagency/ui/mesop/auth/firebase/FirebaseConfig.md) class by passing the necessary values from your Firebase configuration.

    - **Initialize Firebase Authentication**:

        Instiantiate the [**`FirebaseAuth`**](../../../../api/fastagency/ui/mesop/auth/firebase/FirebaseAuth.md) with Google as the sign-in method and pass the Firebase configuration.

        !!! note
            Currently, [**Firebase**](https://firebase.google.com){target="_blank"} is the only supported authentication provider, with Google as the available sign-in method. Future releases will introduce more sign-in options within Firebase.

        - The `allowed_users` parameter controls access to the application, with the following options:

            - String (`str`):

                - To allow a single email address, set `allowed_users="user@example.com"`. Only this user will have access.
                - To permit access for everyone, set `allowed_users="all"`.

            - List of Strings (`list[str]`):

                - Provide a list of authorized email addresses, e.g., `allowed_users=["user1@example.com", "user2@example.com"]`. Only users with these email addresses will be allowed access.

            - Callable (`Callable[[dict[str, Any]], bool]`):

                - This option provides maximum flexibility, allowing you to define custom validation logic. You can pass a function that takes a dictionary and returns a boolean to indicate whether access is granted. This setup supports more complex access checks, such as **database lookups**, **external API checks**, and **custom logic**.

    - **Configure the Mesop UI**:

        MesopUI is set up with a `security_policy`, `custom` styles, and the `auth` configuration. This step ensures that the user interface for the Mesop application is protected by the specified authentication method.


### Complete Application Code

=== "No Authentication"

    <details>
        <summary>main.py</summary>
        ```python
        {!> docs_src/user_guide/ui/mesop/main_mesop.py !}
        ```
    </details>

=== "Basic Authentication"

    <details>
        <summary>main.py</summary>
        ```python
        {!> docs_src/user_guide/ui/mesop/main_mesop_basic_auth.py !}
        ```
    </details>

=== "Firebase Authentication"

    <details>
        <summary>main.py</summary>
        ```python
        {!> docs_src/user_guide/ui/mesop/main_mesop_firebase_auth.py !}
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
=== "No Authentication"

    ![Initial message](../../getting-started/images/chat.png)

=== "Basic Authentication"

    ![Initial message](./images/basic_auth_login.png)
    ![Initial message](./images/basic_auth_chat.png)

=== "Firebase Authentication"

    ![Initial message](./images/auth_login.png)
    ![Initial message](./images/auth_chat.png)

## Debugging Tips
If you encounter issues running the application, ensure that:

- The OpenAI API key is correctly set in your environment variables.
- All necessary packages are installed, especially the `fastagency[autogen,mesop]` dependencies.
- The MesopUI web interface is accessible from the browser, and no firewall is blocking the connection.

---

By using **[MesopUI](../../../../api/fastagency/ui/mesop/MesopUI.md)**, developers can create interactive, web-based multi-agent applications with ease. This interface is ideal for building user-friendly, browser-accessible systems, enabling users to interact with agents in a more engaging and visual environment. You can extend this workflow for more complex scenarios, such as tutoring systems, customer support, or real-time information retrieval.
