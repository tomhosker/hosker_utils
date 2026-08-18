# Standing Orders for Coding Agents

These instructions apply to the entire repository.

## Light infantry mentality

- Work in the spirit of Sharpe's Rifles: use only what the repository and its
  maintainer can reasonably carry.
- Treat speed, straightforwardness, and portability as cardinal virtues.
- Prefer standard-library code, small local scripts, transparent file formats,
  and tools that remain useful without hosted services.
- Add dependencies, abstractions, generated scaffolding, and infrastructure
  only when their concrete value clearly exceeds their carrying cost.
- Choose solutions that are easy to understand, repair, replace, and run on a
  fresh machine. Avoid cleverness that requires a logistical corps.

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
- Treat this repository as a role model for the owner's other repositories.
  Prefer clear, modern, reusable practices and document intentional exceptions.
- Keep the repository small, lightweight, and durable. Prefer checks, builds,
  and automation that run locally and only locally; do not add hosted CI,
  repository bots, or remote automation unless the user explicitly approves a
  concrete need that cannot reasonably be met locally.

## Python conventions

- Support Python 3.11 and newer.
- Follow the existing style and the repository's `ruff.toml`.
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
- Run `python3 -m ruff check .` after Python changes.
- Run `python3 validate.py` when a change affects linted Python code, provided
  it can run safely in the current environment.
- Run `git diff --check` before handing work back.
- Build and inspect the relevant release artifacts after packaging changes.
- If a check cannot be run, state why in the final response.

## Documentation and packaging

- Before declaring a pull request ready, agree the appropriate version bump
  with the user and update the single version in `pyproject.toml`.
- Ensure Python and Debian artifacts derive their version from
  `pyproject.toml`; do not duplicate the version in scripts or configuration.
- Keep installation instructions and supported Python versions accurate.
- Update `README.md` when commands, configuration, or user-visible behaviour
  changes.
- Include package data deliberately; do not add generated files, coverage
  output, build artifacts, logs, or local configuration to Git.
- Keep examples suitable for reuse in other repositories, without introducing
  abstraction merely for its own sake.
