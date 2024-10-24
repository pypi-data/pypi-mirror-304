# glbuild

A lightweight library to collect the entire history of build data and logs from GitLab projects.

## Requirements

- Python 3.10
- [Poetry](https://python-poetry.org/)

## Get started

Install dependencies

```bash
poetry install
```

Access virtual environment

```bash
poetry shell
```

Install pre-commit hook for static code analysis

```bash
pre-commit install
```

## Usage

Install the Python package using Pip

>```bash
>pip install glbuild
>```

Use in a Python script as follows:

```python
import glbuild

glb = glbuild.GitLabBuild(base_url="https://gitlab.com", token="******", projects=[1538, 5427])

glb.start(n_last=100)
```

Use in a Bash command line as follows:

```bash
glbuild --base-url https://gitlab.com --token ****** --output ./data --n-last 100 --project 1538 --project 5427
```

Contracted CLI command:

```bash
glbuild -b https://gitlab.com -t ****** -o ./data -n 100 -p 1538 -p 5427
```
