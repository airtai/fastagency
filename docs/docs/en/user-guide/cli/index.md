## Example Usage

### Running a FastAgency App in Development Mode

```bash
fastagency dev path/to/app.py
```

**Explanation**: This command runs the FastAgency app in **development mode**. It automatically detects the FastAgency app within the specified Python file and runs it with live reload enabled. This is useful for making changes to your code and seeing updates in real-time without needing to restart the server manually. If no file path is provided, FastAgency will try to locate common file names such as `main.py`, `app.py`, or `api.py`.

### Running a FastAgency App with a Specific Workflow

```bash
fastagency run path/to/app.py --workflow simple_workflow
```

**Explanation**: This command runs the FastAgency app in **production mode** and specifies a particular workflow (`simple_workflow`) to execute. This is helpful when you have multiple workflows in your app, and you want to run a specific one. The app can automatically detect the workflow unless you explicitly name it with the `--workflow` option.

### Setting an Initial Message

```bash
fastagency run path/to/app.py --initial_message "Hello, let's start!"
```

**Explanation**: This command allows you to run the app and provide a custom **initial message** to send to the workflow when it starts. The `--initial_message` option is useful when you want to test how your agents respond to different starting inputs, simulating various conversation scenarios. If no message is provided, a default message will be sent.

---

For more information, visit the [**CLI documentation**](../../cli/cli.md).
