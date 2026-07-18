# Other package registries

The package-readiness sequence generalizes across registries: inspect local metadata, scope shipped
files to runtime and documentation, and run an offline build or dry run. Registry availability reads,
authentication, and publication remain closed in this candidate. The commands below are future owner
handoff references only and must not be executed without a new exact approval.

## PyPI (Python)
- Name free? `pip index versions <name>` or check `https://pypi.org/project/<name>/` (404 = free).
- Manifest: `pyproject.toml` (`[project]` name/version/description/readme/license/urls/classifiers).
- What ships: control via `[tool.setuptools.packages.find]` / `MANIFEST.in`; keep tests/fixtures out.
- Dry-run: `python -m build` then `twine check dist/*` (validates metadata + long description render).
- Owner publishes: `twine upload dist/*` (PyPI API token in `~/.pypirc` or `TWINE_*` env — never pasted
  in chat). TestPyPI (`--repository testpypi`) for a rehearsal.

## cargo (Rust)
- Name free? `cargo search <name>` / crates.io. Manifest: `Cargo.toml` (`[package]` + `description`,
  `license`, `repository`, `keywords`, `categories`, `readme`).
- Ship control: `include`/`exclude` in `Cargo.toml`. Dry-run: `cargo publish --dry-run`.
- Owner publishes: `cargo login` then `cargo publish`.

## gem (Ruby)
- Name free? `gem search -r <name>` / rubygems.org. Manifest: `<name>.gemspec` (summary, homepage,
  license, files list). Build: `gem build <name>.gemspec`. Owner publishes: `gem push <name>-x.y.z.gem`.

## Common
- Version must match the CHANGELOG / release candidate (see `releasebench-release-version`).
- Include README image assets referenced by the long-description so the registry page isn't broken.
- The registry page description is a second storefront — keep it consistent with the repo description.
