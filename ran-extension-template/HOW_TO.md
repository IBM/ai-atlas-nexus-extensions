# How to add a new Risk Atals Nexus extension. This is a template to copy.

### Get started
1. Copy the template directory
    ```bash
    cp -r ran-extension-template <YOUR_EXTENSION_NAME>
    ```
2. Change extension package name inside `src/EXTENSION_PACKAGE_NAME`.

2. Modify the pyproject.toml and make appropriate changes. Add your requirements to dependencies.

4. Add new files and sub packages to src/<EXTENSION_PACKAGE_NAME>:
    ```bash
    mkdir src/EXTENSION_PACKAGE_NAME/*

    With an __init__.py in each new directory.
    ```
5. Integrate with the Risk Atlas Nexus API
    - Your extension must use the [Risk Atlas Nexus API](https://github.com/IBM/risk-atlas-nexus) for core functionality.
    - Ensure proper error handling, and logging.

6. Your extension should only be executed via the `run` method of the class `Extension` in `src/EXTENSION_PACKAGE_NAME/main.py`.

6. Add and run tests, linting, formatting and static type checking:
    ```bash
    pytest --cov <YOUR_EXTENSION_NAME> tests # tests
    black --check --line-length 120 src # formatting
    pylint src # linting
    ```

8. Provide unit tests for core functionality in `YOUR_EXTENSION_NAME/tests/` folder inside your extension directory.

7. Update the `YOUR_EXTENSION_NAME/README.md` inside your extension folder with:
    - Name and description
    - Usage instructions
    - License
