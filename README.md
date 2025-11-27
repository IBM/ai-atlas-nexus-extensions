# Risk Atlas Nexus Extensions

<!-- Build Status, is a great thing to have at the top of your repository, it shows that you take your CI/CD as first class citizens -->
<!-- [![Build Status](https://travis-ci.org/jjasghar/ibm-cloud-cli.svg?branch=master)](https://travis-ci.org/jjasghar/ibm-cloud-cli) -->

<!-- Not always needed, but a scope helps the user understand in a short sentance like below, why this repo exists -->
## Scope

The purpose of this project is to provide a template for new open source risk-atlas-nexus extensions.

<!-- This should be the location of the title of the repository, normally the short name -->
## How to add a new Risk Atlas Nexus extension.

Install cookiecutter using pipx package manager in your python environment.
```
pip install pipx
pipx install cookiecutter
```

Use a GitHub template to replicate extension project. Enter the relevant details of your extension. You can change these details later on.
```
pipx run cookiecutter gh:IBM/risk-atlas-nexus-extensions/extension-template
```

Once the extension project is generated, follow the instructions below.

1. Modify the pyproject.toml and make appropriate changes. Add your requirements to dependencies.

2. Add new files and directories to src/<EXTENSION_PACKAGE_NAME>/*
    ```bash
    mkdir src/<EXTENSION_PACKAGE_NAME>/<NEW_SUB_DIRECTORY>

    With an __init__.py in each new directory.
    ```
3. Integrate with the Risk Atlas Nexus API
    - Your extension must use the [Risk Atlas Nexus API](https://github.com/IBM/risk-atlas-nexus) for core functionality.
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
| [Risk Atlas Nexus ARES Intgeration](https://github.com/IBM/ai-atlas-nexus-extensions/tree/main/ran-ares-integration) | AI robustness evaluation, AI risks, red-teaming | ARES Integration for Risk Atlas Nexus allows you to run AI robustness evaluations on AI Systems derived from use cases.|

## Usage

This repository contains some example best practices for open source repositories:

* [LICENSE](LICENSE)
* [README.md](README.md)
* [CONTRIBUTING.md](CONTRIBUTING.md)
* [MAINTAINERS.md](MAINTAINERS.md)
<!-- A Changelog allows you to track major changes and things that happen, https://github.com/github-changelog-generator/github-changelog-generator can help automate the process -->
* [CHANGELOG.md](CHANGELOG.md)

> These are optional

<!-- The following are OPTIONAL, but strongly suggested to have in your repository. -->
* [dco.yml](.github/dco.yml) - This enables DCO bot for you, please take a look https://github.com/probot/dco for more details.
* [travis.yml](.travis.yml) - This is a example `.travis.yml`, please take a look https://docs.travis-ci.com/user/tutorial/ for more details.

These may be copied into a new or existing project to make it easier for developers not on a project team to collaborate.

<!-- A notes section is useful for anything that isn't covered in the Usage or Scope. Like what we have below. -->
## Notes

**NOTE: While this boilerplate project uses the Apache 2.0 license, when
establishing a new repo using this template, please use the
license that was approved for your project.**

**NOTE: This repository has been configured with the [DCO bot](https://github.com/probot/dco).
When you set up a new repository that uses the Apache license, you should
use the DCO to manage contributions. The DCO bot will help enforce that.
Please contact one of the IBM GH Org stewards.**

<!-- Questions can be useful but optional, this gives you a place to say, "This is how to contact this project maintainers or create PRs -->
If you have any questions or issues you can create a new [issue here][issues].

Pull requests are very welcome! Make sure your patches are well tested.
Ideally create a topic branch for every separate change you make. For
example:

1. Fork the repo
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Added some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create new Pull Request

## License

All source files must include a Copyright and License header. The SPDX license header is 
preferred because it can be easily scanned.

If you would like to see the detailed LICENSE click [here](LICENSE).

```text
#
# Copyright IBM Corp. {Year project was created} - {Current Year}
# SPDX-License-Identifier: Apache-2.0
#
```
## Authors

Optionally, you may include a list of authors, though this is redundant with the built-in
GitHub list of contributors.

- Author: New OpenSource IBMer <new-opensource-ibmer@ibm.com>

[issues]: https://github.com/IBM/repo-template/issues/new
