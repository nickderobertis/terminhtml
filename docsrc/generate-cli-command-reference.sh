#!/bin/bash
cd ..
typer terminhtml/cli_docs.py utils docs --name terminhtml --output docsrc/source/commands.md
cd docsrc
