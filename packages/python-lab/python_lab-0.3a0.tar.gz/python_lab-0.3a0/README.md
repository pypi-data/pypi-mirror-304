# Python Lab

A workspace dedicated to experimenting with and exploring Python concepts.

## Setup

### 1. Create a Virtual Environment

To get started, create and activate a virtual environment to manage project dependencies:

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

## Setup

```bash
pip install -r requirements.txt
```

## Run Tests

```bash
PYTHONPATH=. pytest test/test_shapes.py
```

## Create a Distribution Package

```bash
pip install setuptools wheel
```

## Then build your package

```bash
python setup.py sdist bdist_wheel
```

## Upload to PyPI: 
(Create an account on PyPI if you don't have, then upload your package using twine)

```bash
pip install twine
twine upload dist/*
```