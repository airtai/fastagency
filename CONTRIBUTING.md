> **_NOTE:_**  This is an auto-generated file. Please edit docs/docs/en/contributing/CONTRIBUTING.md instead.

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
