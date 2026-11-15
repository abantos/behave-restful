# Releasing

Releases are published to PyPI by `.github/workflows/python-release-pypi.yml` when a GitHub release is **published**.

## Process

1. Bump the version in `behave_restful/about.py` and merge to `master`.
2. Create and publish a GitHub release for the new version.
3. The workflow builds the wheel and sdist, validates them with `twine check`, and publishes them using
   [PyPI Trusted Publishing](https://docs.pypi.org/trusted-publishers/) (OIDC). No API token is used.
4. PyPI Publish Attestations ([PEP 740](https://peps.python.org/pep-0740/)) are generated automatically for every distribution.

The PyPI project must have a Trusted Publisher configured for owner `abantos`, this repository, and workflow
`python-release-pypi.yml`, with the environment field left blank.

## Verifying provenance

On PyPI, open the project's **Security** tab (or each file's details) and confirm the attestation names this
repository and workflow for both the wheel and the sdist.

To verify from the command line:

```bash
python -m pip install pypi-attestations
pypi-attestations verify pypi \
  --repository https://github.com/abantos/behave-restful \
  https://files.pythonhosted.org/path/to/distribution
```

Repeat for the wheel and the source distribution.
