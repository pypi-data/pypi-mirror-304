# python package template

[![ci](https://github.com/fopina/example/actions/workflows/publish-main.yml/badge.svg)](https://github.com/fopina/example/actions/workflows/publish-main.yml)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/fp-github-template-example.svg)](https://pypi.python.org/pypi/fp-github-template-example/)
[![PyPI version](https://badge.fury.io/py/fp-github-template-example.svg)](https://badge.fury.io/py/fp-github-template-example)
[![Very popular](https://img.shields.io/pypi/dm/fp-github-template-example)](https://pypistats.org/packages/fp-github-template-example)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Content

* `pytest` for tests: `make test`
* `ruff` for linting/formatting: `make lint` (replaces both `black` and `isort`)
* `.github` with actions ready to be used
    * [test](.github/workflows/test.yml) runs lint checks and unit tests
    * [publish-dev](.github/workflows/publish-dev.yml) publishes feature branches (`dev`/`dev-*`) to [testpypi](https://test.pypi.org)
    * [publish-main](.github/workflows/publish-main.yml) publishes semver tags to [pypi](https://pypi.org)

## New project checklist

* [ ] Replace folder `example` with the actual package
* [ ] Replace `LICENSE` if MIT does not apply
* [ ] Search the project for `# TODO` to find the (minimum list of) places that need to be changed.
* [ ] Add PYPI credentials to secrets
    * `PYPI_USERNAME` and `PYPI_TOKEN` to publish tags to pypi
    * `TESTPYPI_USERNAME` and `TESTPYPI_TOKEN` to publish dev branches to testpypi
