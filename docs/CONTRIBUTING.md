# Contributing to Split Raster

Thanks for helping improve `splitraster`. This guide is for developers who want to
change code, tests, documentation, or release tooling.

## Branching Model

This repository uses a simple develop-to-release flow:

- `develop` is the integration branch for day-to-day development.
- `feature/*` and `codex/*` branches are used for focused changes.
- `master` is the stable release branch.
- `v*` tags trigger package release, for example `v0.4.1`.

Start new work from `develop`:

```bash
git switch develop
git pull
git switch -c feature/your-change
```

Keep changes small and reviewable. Separate unrelated bug fixes, workflow changes,
documentation updates, and releases into different branches when practical.

## Development Environment

The project requires Python 3.10 or newer and uses `uv` for dependency management.

```bash
uv sync
```

Run commands through `uv run` so they use the project environment:

```bash
uv run pytest tests/ -v
uv run ruff check .
uv run ruff format --check .
```

Optional GeoTIFF support requires GDAL:

```bash
uv pip install "splitraster[geo]"
```

GDAL often needs system packages as well. If your change does not touch
`src/splitraster/geo.py`, it is acceptable to run the regular test suite without a
local GDAL install.

## Quality Checks

Before opening a pull request, run:

```bash
uv run ruff check .
uv run ruff format --check .
uv run pytest tests/ -v
```

For packaging-related changes, also run:

```bash
uv run python -m build
uv run python -m twine check dist/*
```

The CI workflow repeats the important checks on Python 3.10, 3.11, 3.12, and 3.13.

## Tests

Tests should avoid writing generated files into tracked sample-data directories.
Use `tmp_path` for output created during tests.

Add or update tests when changing:

- tile naming or overwrite behavior
- crop size, stride, padding, or overlap behavior
- random crop pairing between image and label
- GeoTIFF read/write behavior
- package metadata, build, or release workflow behavior

GeoTIFF logic can be covered with fake GDAL objects when the test only needs to
verify control flow. Use real GDAL integration tests only when the file I/O itself
is the behavior under test.

## Pull Requests

Open pull requests into `develop` unless the maintainer asks for a different
target branch.

A good pull request includes:

- a concise description of the change
- the reason for the change
- tests that were run
- any remaining risks, especially around GDAL or release automation

## Versioning

The package version is maintained in one place:

```toml
# pyproject.toml
[project]
version = "0.4.1"
```

Do not edit `src/splitraster/__init__.py` to bump the version. The package
`__version__` is read from installed package metadata.

Use semantic versioning in spirit:

- patch version for bug fixes and documentation-only release corrections
- minor version for backward-compatible features
- major version for breaking API or output-format changes

## Release Process

Releases are tag-driven. The release workflow runs only for tags matching `v*`.
It also verifies that the tag matches the version in `pyproject.toml`.

For example, to release `0.4.1`:

```bash
# Update pyproject.toml:
# version = "0.4.1"

git add pyproject.toml
git commit -m "Bump version to 0.4.1"

# After the release commit is on master:
git tag v0.4.1
git push origin master
git push origin v0.4.1
```

The release workflow will:

1. build the source distribution and wheel once
2. validate distribution metadata with `twine check`
3. test the built wheel on Python 3.10 through 3.13
4. publish to PyPI with Trusted Publishing/OIDC
5. create a GitHub Release with the same artifacts

PyPI Trusted Publishing must be configured for:

- repository: `cuicaihao/split_raster`
- workflow: `python-CD.yml`
- environment: `pypi`

## Documentation

Documentation source files live in `docs/` and are built with MkDocs. Treat
documentation like code: edit the source Markdown and image files, then let the
docs workflow publish the generated site.

Repository layout:

- `docs/` contains tracked documentation source files.
- `mkdocs.yml` contains navigation and MkDocs configuration.
- `site/` is local build output and should stay untracked.
- `gh-pages` is the deployment branch for generated GitHub Pages content.

Do not manually edit generated files in `site/` or on `gh-pages`. Make the change
in `docs/`, verify it locally, and let the workflow publish it.

```bash
uv run mkdocs serve
uv run mkdocs build
```

Documentation deploy is handled separately from package release and runs from the
docs workflow.
