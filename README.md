# JSON with Comments for Python
[![pypi version](https://img.shields.io/pypi/v/json-with-comments.svg)](https://pypi.python.org/project/json-with-comments)
[![Python package](https://github.com/n-takumasa/json-with-comments/actions/workflows/test.yml/badge.svg)](https://github.com/n-takumasa/json-with-comments/actions/workflows/test.yml)
[![Python Versions](https://img.shields.io/pypi/pyversions/json-with-comments.svg)](https://pypi.org/project/json-with-comments/)

## Features
* `load()`, `loads()`
  * Remove single line (`//`) and block comments (`/* */`)
  * Remove trailing commas from arrays and objects
* `dump()`, `dumps()`
  * Add comments
  * Add trailing commas

## Usage

```sh
pip install json-with-comments
```

```py
>>> import jsonc
>>> jsonc.loads("{// comment \n}")
{}
>>> jsonc.loads("{/* comment */}")
{}
>>> jsonc.loads('{"spam": "ham // egg" /* comment */}')
{'spam': 'ham // egg'}
>>> jsonc.loads('{"spam": /* comment */"ham /* egg */"}')
{'spam': 'ham /* egg */'}
```
And just like `json` module
