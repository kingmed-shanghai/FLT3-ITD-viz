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

