from __future__ import annotations

import re

def _make_pattern(s: str, /):
    return re.compile(s, re.DOTALL | re.VERBOSE)

_REMOVE_C_COMMENT = _make_pattern(r"""
    ( # String Literal
        \"(?:\\.|[^\\\"])*?\"
    )
    |
    ( # Comment
        \/\*.*?\*\/
        |
        \/\/[^\r\n]*?(?:[\r\n])
    )
    """)


_REMOVE_TRAILING_COMMA = _make_pattern(r"""
    ( # String Literal
        \"(?:\\.|[^\\\"])*?\"
    )
    | # Right Brace without Trailing Comma & Spaces
    ,\s*([\]}])
""")


_ADD_TRAILING_COMMA = _make_pattern(r"""
    ( # String Literal
        \"(?:\\.|[^\\\"])*?\"
    )
    | # Don't match opening braces to avoid {,}
    ((?<=\")|[^,\[{\s])
    (?=\s*([\]}]))
""")


def _remove_c_comment(text: str) -> str:
    if text[-1] != "\n":
        text = text + "\n"
    return _REMOVE_C_COMMENT.sub(lambda x: x.group(1), text)


def _remove_trailing_comma(text: str) -> str:
    return _REMOVE_TRAILING_COMMA.sub(lambda x: x.group(1) or x.group(2), text)


def _add_trailing_comma(text: str) -> str:
    return _ADD_TRAILING_COMMA.sub(lambda x: x.group(1) or x.group(2) + ",", text)
