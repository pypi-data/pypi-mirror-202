# Voliboli PDF Scraper

## Tests

You can run test from the root of this repository using:

    pipenv run python tests/test_main.py

## Distribute

To generate the distribution archives, run:

    python3 -m pip install --upgrade build
    python3 -m build

You can then install this package locally from any other project using:

    pip install -e /path/to/root

where `root` is the top-level directory of this project.

## New Release

To deploy a new version you can use the following commands:

    twine upload --skip-existing dist/*
