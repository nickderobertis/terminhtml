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

```{include} ../../README.md
```

For more information on getting started, take a look at the tutorial and examples.

## Tutorial and Examples

Render rich output:

```shell
terminhtml "python -m rich"
```

```{terminhtml}
python -m rich
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
terminhtml "$(<demo-script.sh)"
```

Allow longer-running commands:

```shell
terminhtml -t 20 "sleep 15 && echo woo"
```

Echo the commands to stdout:

```shell
terminhtml -e "echo foo"
```


```{toctree}
---
maxdepth: 2
---

tutorial
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
