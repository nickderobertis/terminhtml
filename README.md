

[![](https://codecov.io/gh/nickderobertis/terminhtml/branch/main/graph/badge.svg)](https://codecov.io/gh/nickderobertis/terminhtml)
[![PyPI](https://img.shields.io/pypi/v/terminhtml)](https://pypi.org/project/terminhtml/)
![PyPI - License](https://img.shields.io/pypi/l/terminhtml)
[![Documentation](https://img.shields.io/badge/documentation-pass-green)](https://nickderobertis.github.io/terminhtml/)
![Tests Run on Ubuntu Python Versions](https://img.shields.io/badge/Tests%20Ubuntu%2FPython-3.8%20%7C%203.9%20%7C%203.10-blue)
![Tests Run on Macos Python Versions](https://img.shields.io/badge/Tests%20Macos%2FPython-3.8%20%7C%203.9%20%7C%203.10-blue)
[![Github Repo](https://img.shields.io/badge/repo-github-informational)](https://github.com/nickderobertis/terminhtml/)

#  TerminHTML

<div align="center">
  <p align="center">
    <a href="https://nickderobertis.github.io/terminhtml/">
      <img src="https://nickderobertis.github.io/terminhtml/_static/images/demo-output.gif" alt="TerminHTML example GIF">
    </a>
  </p>
  <sub>This GIF doesn't do TerminHTML justice, check out the full version <a href="https://nickderobertis.github.io/terminhtml/">in the docs</a></sub>
</div>

## Overview

Run shell commands and convert into an HTML/CSS animated terminal

## Getting Started

Install `terminhtml`. Recommended installation is with 
[pipx](https://github.com/pypa/pipx) but can also be done via `pip`:

```
pipx install terminhtml
```

A simple example:

```shell
terminhtml "echo 'Hello World'"
```

See 
[more examples in the documentation.](
https://nickderobertis.github.io/terminhtml/
)

## Development Status

This project is currently in early-stage development. There may be
breaking changes often. While the major version is 0, minor version
upgrades will often have breaking changes.

## Developing

First ensure that you have `pipx` installed, if not, install it with `pip install pipx`.

Then clone the repo and run `npm install` and `pipenv sync`. Run `pipenv shell`
to use the virtual environment. Make your changes and then run `nox` to run formatting,
linting, and tests.

Develop documentation by running `nox -s docs` to start up a dev server.

To run tests only, run `nox -s test`. You can pass additional arguments to pytest
by adding them after `--`, e.g. `nox -s test -- -k test_something`.

## Author

Created by Nick DeRobertis. MIT License.

## Related Projects

- [terminhtml-js](https://github.com/nickderobertis/terminhtml-js) - The JavaScript frontend for TerminHTML, but can also be used standalone
- [terminhtml-bootstrap](https://github.com/nickderobertis/terminhtml-bootstrap) - A script that loads TerminHTML in the browser with default settings
- [sphinx-terminhtml](https://nickderobertis.github.io/sphinx-terminhtml/) - A Sphinx directive for using TerminHTML in Sphinx projects

## Links

See the
[documentation here.](
https://nickderobertis.github.io/terminhtml/
)
