> **_NOTE:_**  This is an auto-generated file. Please edit docs/docs/en/contributing/CONTRIBUTING.md instead.

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
