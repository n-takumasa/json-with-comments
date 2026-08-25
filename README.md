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
* Parity with built-in `json` module

## Usage

### Installation

```sh
pip install json-with-comments
```

### Loading JSON with comments

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

### Saving JSON with comments

`dump()` and `dumps()` support these additional arguments:

#### `trailing_comma`

Allows adding trailing commas to every element

Example:

```py
import jsonc

print(
    jsonc.dumps(
        {"a": 1, "b": 2},
        indent=2,
        trailing_comma=True,
    )
)
```

Output:

```jsonc
{
  "a": 1,
  "b": 2,
}
```

#### `comments`

Allows adding comments to generated JSON

It can be:
* A dictionary containing comments for nested elements
* A string containing the comment
* A tuple combining the string and the dictionary

**Attention**: it is not possible to add comments to JSON that is not indented (`indent=` not set).

Simple example with dictionary:

```py
import jsonc

print(
    jsonc.dumps(
        {"a": 1, "b": 2},
        indent=2,
        comments={
            "a": "this is a",
            "b": "this is b",
        },
    )
)
```

Output:
```jsonc
{
  // this is a
  "a": 1,
  // this is b
  "b": 2
}
```

Example with tuple commenting the list as a whole and the elements:

```py
import jsonc

print(
    jsonc.dumps(
        ["x", "y", "z"],
        indent=2,
        comments=(
            "the list",
            {
                0: "element #0",
                1: "element #1",
                2: "element #2",
            },
        ),
    )
)
```

Output:

```jsonc
// the list
[
  // element #0
  "x",
  // element #1
  "y",
  // element #2
  "z"
]
```
