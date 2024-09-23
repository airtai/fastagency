# `fastagency`

FastAgency CLI - The **fastapi** command line app. 😎

Manage your **FastAgency** projects, run your FastAgency apps, and more.

Read more in the docs: [https://fastagency.ai/latest/](https://fastagency.ai/latest/).

**Usage**:

```console
$ fastagency [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--version`: Show the version and exit.
* `--help`: Show this message and exit.

**Commands**:

* `dev`: Run a **FastAgency** app in <code>development</code> mode.
* `run`: Run a **FastAgency** app in <code>production</code> mode.
* `version`: Display the version of FastAgency

## `fastagency dev`

Run a **FastAgency** app in <code>development</code> mode. 🚀

This is similar to the **fastagency run** command but with **reload** enabled and listening on the <code>127.0.0.1</code> address.

It automatically detects the Python module or package that needs to be imported based on the file or directory path passed.

If no path is passed, it tries with:

- <code>main.py</code>
- <code>app.py</code>
- <code>api.py</code>
- <code>app/main.py</code>
- <code>app/app.py</code>
- <code>app/api.py</code>

It also detects the directory that needs to be added to the **PYTHONPATH** to make the app importable and adds it.

It detects the **FastAgency** app object to use. By default it looks in the module or package for an object named:

- <code>app</code>
- <code>api</code>

Otherwise, it uses the first **FastAgency** app found in the imported module or package.

**Usage**:

```console
$ fastagency dev [OPTIONS] [PATH]
```

**Arguments**:

* `[PATH]`: A path to a Python file or package directory (with <code>__init__.py</code> files) containing a **FastAgency** app. If not provided, a default set of paths will be tried.

**Options**:

* `--app TEXT`: The name of the variable that contains the **** app in the imported module or package. If not provided, it is detected automatically.
* `-w, --workflow TEXT`: The name of the workflow to run. If not provided, the default workflow will be run.
* `-i, --initial_message TEXT`: The initial message to send to the workflow. If not provided, a default message will be sent.
* `--help`: Show this message and exit.

## `fastagency run`

Run a **FastAgency** app in <code>production</code> mode. 🚀

This is similar to the **fastagency dev** command, but optimized for production environments.

It automatically detects the Python module or package that needs to be imported based on the file or directory path passed.

If no path is passed, it tries with:

- <code>main.py</code>
- <code>app.py</code>
- <code>api.py</code>
- <code>app/main.py</code>
- <code>app/app.py</code>
- <code>app/api.py</code>

It also detects the directory that needs to be added to the **PYTHONPATH** to make the app importable and adds it.

It detects the **FastAgency** app object to use. By default it looks in the module or package for an object named:

- <code>app</code>
- <code>api</code>

Otherwise, it uses the first **FastAgency** app found in the imported module or package.

**Usage**:

```console
$ fastagency run [OPTIONS] [PATH]
```

**Arguments**:

* `[PATH]`: A path to a Python file or package directory (with <code>__init__.py</code> files) containing a **FastAgency** app. If not provided, a default set of paths will be tried.

**Options**:

* `--app TEXT`: The name of the variable that contains the **** app in the imported module or package. If not provided, it is detected automatically.
* `-w, --workflow TEXT`: The name of the workflow to run. If not provided, the default workflow will be run.
* `-i, --initial_message TEXT`: The initial message to send to the workflow. If not provided, a default message will be sent.
* `--help`: Show this message and exit.

## `fastagency version`

Display the version of FastAgency

**Usage**:

```console
$ fastagency version [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.
