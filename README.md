# FLT3-ITD-viz

## Dev

Prerequisites

- [Poetry](https://python-poetry.org/)
- [pyenv](https://github.com/pyenv/pyenv)

```bash
git clone https://github.com/kingmed-shanghai/FLT3-ITD-viz.git
cd FLT3-ITD-viz

pyenv install 3.12
poetry env use $(pyenv which python)

cat <<EOF > ".env"
export GPG_TTY=\$(tty)
export PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring
source \$(poetry env info --path)/bin/activate
EOF

source .env
poetry install
pre-commit install
pre-commit run --all-files
```

## Dash IGV Visualization

Run example Dash app:

```python
python -m tests.test_igv
```

For detailed information on the Dash application for genomic data visualization using the Integrative Genomics Viewer (IGV), please refer to documentation in [`docs/dash_igv.md`](docs/dash_igv.md).

This documentation provides an overview, usage instructions, and a detailed explanation of the key components of our Dash IGV visualization app. It's an excellent resource for understanding how to interact with and utilize the app effectively for genomic data exploration.

