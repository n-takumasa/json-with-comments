r"""JSON with Comments for Python

    >>> import jsonc
    >>> jsonc.loads("{// comment \n}")
    {}
    >>> jsonc.loads("{/* comment */}")
    {}
    >>> jsonc.loads('{"spam": "ham // egg" /* comment */}')
    {'spam': 'ham // egg'}
    >>> jsonc.loads('{"spam": /* comment */"ham /* egg */"}')
    {'spam': 'ham /* egg */'}
"""

from __future__ import annotations

from typing import TextIO

__version__ = "1.0.0"
import json
import re
from json import dump, dumps  # for compatibility

_REMOVE_C_COMMENT = r"""
    ( # String Literal
        \"(?:[^\\\"]|\\\"|\\\\|\\)*?\"
    )
    |
    ( # Comment
        \/\*.*?\*\/
        |
        \/\/[^\r\n]*?(?:[\r\n]|\Z)
    )
    """


_REMOVE_TRAILING_COMMA = r"""
    ( # String Literal
        \"(?:[^\\\"]|\\\"|\\\\|\\)*?\"
    )
    | # Right Brace without Trailing Comma & Spaces
    ,\s*([\]}])
"""


def _remove_c_comment(text: str) -> str:
    return re.sub(_REMOVE_C_COMMENT, lambda x: x.group(1), text, flags=re.DOTALL | re.VERBOSE)


def _remove_trailing_comma(text: str) -> str:
    return re.sub(_REMOVE_TRAILING_COMMA, lambda x: x.group(1) or x.group(2), text, flags=re.DOTALL | re.VERBOSE)


def load(
    fp: TextIO,
    *,
    cls=None,
    object_hook=None,
    parse_float=None,
    parse_int=None,
    parse_constant=None,
    object_pairs_hook=None,
    **kw,
):
    """Deserialize ``fp`` (a ``.read()``-supporting file-like object containing
    a JSON document) to a Python object.

    Reference: ``json.load``
    """
    return json.loads(
        _remove_trailing_comma(_remove_c_comment(fp.read())),
        cls=cls,
        object_hook=object_hook,
        parse_float=parse_float,
        parse_int=parse_int,
        parse_constant=parse_constant,
        object_pairs_hook=object_pairs_hook,
        **kw,
    )


def loads(
    s: str,
    *,
    cls=None,
    object_hook=None,
    parse_float=None,
    parse_int=None,
    parse_constant=None,
    object_pairs_hook=None,
    **kw,
):
    """Deserialize ``s`` (a ``str``, ``bytes`` or ``bytearray`` instance
    containing a JSON document) to a Python object.

    Reference: ``json.loads``
    """
    return json.loads(
        _remove_trailing_comma(_remove_c_comment(s)),
        cls=cls,
        object_hook=object_hook,
        parse_float=parse_float,
        parse_int=parse_int,
        parse_constant=parse_constant,
        object_pairs_hook=object_pairs_hook,
        **kw,
    )
