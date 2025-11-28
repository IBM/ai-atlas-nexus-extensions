# AI Atlas Nexus Extensions

<!-- Build Status, is a great thing to have at the top of your repository, it shows that you take your CI/CD as first class citizens -->
<!-- [![Build Status](https://travis-ci.org/jjasghar/ibm-cloud-cli.svg?branch=master)](https://travis-ci.org/jjasghar/ibm-cloud-cli) -->

<!-- Not always needed, but a scope helps the user understand in a short sentance like below, why this repo exists -->
## Scope

The purpose of this project is to provide a template for new open source ai-atlas-nexus extensions.

<!-- This should be the location of the title of the repository, normally the short name -->
## How to add a new AI Atlas Nexus extension.

Install cookiecutter using pipx package manager in your python environment.
```
pip install pipx
pipx install cookiecutter
```

Use a GitHub template to replicate extension project. Enter the relevant details of your extension. You can change these details later on.
```
pipx run cookiecutter gh:IBM/ai-atlas-nexus-extensions/extension-template
```

Once the extension project is generated, follow the instructions below.

1. Modify the pyproject.toml and make appropriate changes. Add your requirements to dependencies.

2. Add new files and directories to src/<EXTENSION_PACKAGE_NAME>/*
    ```bash
    mkdir src/<EXTENSION_PACKAGE_NAME>/<NEW_SUB_DIRECTORY>

    With an __init__.py in each new directory.
    ```
3. Integrate with the AI Atlas Nexus API
    - Your extension must use the [AI Atlas Nexus API](https://github.com/IBM/ai-atlas-nexus) for core functionality.
    - Ensure proper error handling, and logging.

4. Your extension should only be executed via the `run` method of the class `Extension` in `src/EXTENSION_PACKAGE_NAME/main.py`.

5. Add and run tests, linting, formatting and static type checking:
    ```bash
    pytest --cov <YOUR_EXTENSION_NAME> tests # tests
    black --check --line-length 120 src # formatting
    pylint src # linting
    ```

6. Provide unit tests for core functionality in `YOUR_EXTENSION_NAME/tests/` folder inside your extension directory.

7. Update the `<YOUR_EXTENSION_NAME>/README.md` inside your extension folder with:
    - Name and description
    - Usage instructions
    - License

## Extension list

| Name| Tags | Description|
| :--- |  :--- | :--- |
| [AI Atlas Nexus ARES Intgeration](https://github.com/IBM/ai-atlas-nexus-extensions/tree/main/ran-ares-integration) | AI robustness evaluation, AI risks, red-teaming | ARES Integration for AI Atlas Nexus allows you to run AI robustness evaluations on AI Systems derived from use cases.|


## License
AI Atlas Nexus Extensions is under Apache 2.0 license.


[View the detailed LICENSE](LICENSE).


## IBM ❤️ Open Source AI

AI Atlas Nexus has been brought to you by IBM.
