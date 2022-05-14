% terminhtml documentation master file, created by
%   copier-pypi-sphinx-flexlate.
%   You can adapt this file completely to your liking, but it should at least
%   contain the root `toctree` directive.

# Welcome to TerminHTML documentation!

```{terminhtml}
---
prompt-matchers: "['\\[0m: ']"
input: "Nick DeRobertis"
cwd: ..
disable-cache:
---
python -m terminhtml.demo_output
```

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

For more information on getting started, take a look at the tutorial and examples.

## Tutorial and Examples

Render rich output:

```shell
terminhtml "python -m rich.color"
```

```{terminhtml}
python -m rich.color
```

Progress bars work too:

```shell
terminhtml "python -m rich.progress_bar"
```

```{terminhtml}
python -m rich.progress_bar
```

Animate prompts and user input:

```shell
terminhtml -m "] " -i "woo" "read -p '[value?] ' varname && echo \$varname"
```

```{terminhtml}
---
input: woo
prompt-matchers: "['] ']"
---
read -p '[value?] ' varname && echo $varname
```

Run setup commands before the animated session:

```shell
terminhtml "cat woo.txt" -s "echo a > woo.txt && echo b >> woo.txt"
```

```{terminhtml}
---
setup: "echo a > woo.txt && echo b >> woo.txt"
---
cat woo.txt
```

Output results to a file: 

```shell
terminhtml -o output.html "echo woo"
```

Run commands in a specific directory rather than a temporary directory

```shell
terminhtml -c .. "ls -l"
```

```{terminhtml}
---
cwd: ..
---
ls -l
```

Run a script:

```shell
terminhtml "$(<my-script.sh)"
```

Allow longer-running commands:

```shell
terminhtml -t 20 "sleep 15 && echo woo"
```

Echo the commands to stdout:

```shell
terminhtml -e "echo foo"
```

Take a look at the [CLI Reference](commands.md) for more information.

To use the Python API, take a look at the TerminHTML class in the main module 
[in the API reference](api/terminhtml.rst).

## Development Status

This project is currently in early-stage development. There may be
breaking changes often. While the major version is 0, minor version
upgrades will often have breaking changes.

## Author

Created by Nick DeRobertis. MIT License.

```{toctree}
---
maxdepth: 2
---
CLI Reference <commands>
```

## API Documentation

```{eval-rst}
.. toctree:: api/modules
   :maxdepth: 3
```

## Indices

- {ref}`genindex`
- {ref}`modindex`
- {ref}`search`
