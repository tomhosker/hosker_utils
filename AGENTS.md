# Standing Orders for Coding Agents

These instructions apply to the entire repository.

## Communication

- Be encouraging at all times, and funny wherever possible.
- State meaningful assumptions and call out risky or system-changing commands
  before running them.
- Summarize changed files and verification results when handing work back.

## Working approach

- Read this file and `README.md` before making changes.
- Inspect the current Git status before editing. Preserve user changes and keep
  unrelated work out of the diff.
- Prefer small, focused changes that preserve existing public behaviour unless
  the task explicitly requires a breaking change.
- Do not commit, push, publish packages, alter Git history, or run commands that
  require `sudo` unless the user explicitly asks.
- Do not run the HMSS installer or the repository-backup commands as part of
  verification; they change the host system or external repositories.

## Python conventions

- Support Python 3.11 and newer.
- Follow the existing style and the repository's `pylintrc`.
- Add type hints to new or changed public functions where practical.
- Use `pathlib.Path` for filesystem paths and specify UTF-8 when opening text
  files.
- Keep subprocess arguments as lists and use `check=True` when failure should
  stop the operation.

## Tests and verification

- Add or update tests for behaviour changes and bug fixes.
- Tests must not write to the user's home directory, invoke `sudo`, access the
  network, or modify real Git repositories. Use temporary paths and mocks.
- Run `python3 -m pytest` after Python changes.
- Run `python3 validate.py` when a change affects linted Python code, provided
  it can run safely in the current environment.
- Run `git diff --check` before handing work back.
- If a check cannot be run, state why in the final response.

## Documentation and packaging

- Keep installation instructions and supported Python versions accurate.
- Update `README.md` when commands, configuration, or user-visible behaviour
  changes.
- Include package data deliberately; do not add generated files, coverage
  output, build artifacts, logs, or local configuration to Git.
