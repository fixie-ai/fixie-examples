# This is the main Justfile for the Fixie Examples repo.
# It contains helpful scripts and recipes for maintaining the tree.
# Using Just is not necessary if you are just using the examples.
# To install Just, see: https://github.com/casey/just#installation 

# This causes the .env file to be read by Just.
set dotenv-load := true

# Allow for positional arguments in Just receipes.
set positional-arguments := true

# Default recipe that runs if you type "just".
default: format check typecheck

# Install dependencies for local development.
install:
    pip install poetry
    poetry install --sync

# Format code.
format:
    poetry run autoflake . --remove-all-unused-imports --quiet --in-place -r --exclude third_party
    poetry run isort . --force-single-line-imports
    poetry run black .

# Run code formatting checks.
check:
    poetry run black . --check
    poetry run isort . --check --force-single-line-imports
    poetry run autoflake . --check --quiet --remove-all-unused-imports -r --exclude third_party

# Run typechecking on each agent subdirectory independently.
typecheck:
    #!/usr/bin/env bash
    set -eux -o pipefail
    for dir in `find agents -type d -depth 1`; do poetry run mypy $dir; done

# Run a Python REPL in the Poetry environment.
python:
    poetry run python

# Run the poetry command with the local .env loaded.
poetry *FLAGS:
    poetry {{FLAGS}}

# Run a new shell with the Poetry Pyenv environment and .env file loaded.
shell:
    poetry shell

# Run tests.
test PATH=".":
    poetry run pytest -n auto {{PATH}}
