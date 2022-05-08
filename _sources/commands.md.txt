# `terminhtml`

Create an animated HTML/CSS terminal by running commands and recording their output.

Examples:
```
# Run two commands
$ terminhtml "echo woo > something.txt" "cat something.txt"

# Output results to a file
$ terminhtml -o output.html "echo woo"

# Run a script my-script.sh
$ terminhtml "$(<my-script.sh)"

# Run setup commands before the animated session
$ terminhtml "cat woo.txt" -s "echo a > woo.txt && echo b >> woo.txt"

# Output partial HTML
$ terminhtml -p "echo woo"

# Allow longer-running commands
$ terminhtml -t 20 "sleep 15 && echo woo"

# Animate commands that prompt for user input
$ terminhtml -m "] " -i "woo" "read -p '[value?] ' varname && echo \$varname"
```

**Usage**:

```console
$ terminhtml [OPTIONS] COMMANDS...
```

**Arguments**:

* `COMMANDS...`: Commands to run  [required]

**Options**:

* `-s, --setup TEXT`: Setup commands that are run before the animated session: the IO from these commands are not displayed but can be used to set up the session in a particular state before the animation.
* `-i, --input TEXT`: Input to be passed to the commands. Input is to be passed as a list that will be matched up to commands in order. If you need to provide multiple inputs to one command, separate them by \n within the same input item. Note that you must use prompt matchers for input to do anything.
* `-a, --allow-exceptions`: Allow exceptions from passed commands, still generate html
* `-m, --prompt-matchers TEXT`: Regex patterns to match prompts. When prompts are matched, they will be provided the passed input.
* `-t, --timeout INTEGER`: Timeout in seconds for each command.  [default: 10]
* `-o, --out PATH`: Output path, defaults to printing to stdout
* `-p, --partial`: Whether to output HTML for only the the commands themselves, defaults to full HTML including JS/CSS/full page structure
* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.
