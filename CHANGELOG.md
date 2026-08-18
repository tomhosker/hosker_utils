# Changelog

## 2.7.0 — 2026-08-18

- Replaced legacy `setup.py` packaging with declarative `pyproject.toml`
  metadata and proper console entry points.
- Replaced Pylint with Ruff and raised the enforced test coverage floor to
  80%.
- Added isolated release tooling for building and validating PyPI artifacts.
- Added a native Debian package builder with synchronized version metadata,
  runtime dependencies, and a bundled Ruff executable where APT cannot provide
  one.
- Made tests hermetic and expanded coverage of command, installer, dependency,
  backup, and continuous-integration behaviour.
- Added repository standing orders and documented the project's role-model
  conventions.

Earlier releases predate this changelog. Their history remains available on
[PyPI](https://pypi.org/project/hosker-utils/#history).
