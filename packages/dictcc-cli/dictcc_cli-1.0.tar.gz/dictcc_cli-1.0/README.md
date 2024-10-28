# dictcc-cli

[![PyPI - Version](https://img.shields.io/pypi/v/dictcc-cli)](https://pypi.org/project/dictcc-cli/)

`dictcc-cli` is a command-line tool that scrapes dict.cc for translations and displays results in a colourful table.

## Installation

Requires Python version 3.11 or higher and pip.

```bash
pip install dictcc
```

## Usage

Two-way search in English and German:

```bash
dictcc water
```

Search between a specified language and German:

```bash
dictcc -l fr Wasser
```

Search between two specified languages:

```bash
dictcc -l fr -l en eau
```

## License

`dictcc-cli` is distributed under the terms of the MIT License.
