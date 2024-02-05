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

import json
import warnings
from json import JSONDecodeError, JSONDecoder, JSONEncoder
from typing import TYPE_CHECKING

from jsonc._add_comments import _add_comments
from jsonc._util import _add_trailing_comma, _remove_c_comment, _remove_trailing_comma

if TYPE_CHECKING:
    from collections.abc import Callable
    from typing import Any, TextIO

    from jsonc._add_comments import Comments

__version__ = "0.0.0"
__all__ = [
    "dump",
    "dumps",
    "load",
    "loads",
    "JSONDecoder",
    "JSONDecodeError",
    "JSONEncoder",
]


def load(
    fp: TextIO,
    *,
    cls: type[json.JSONDecoder] | None = None,
    object_hook: Callable[[dict[Any, Any]], Any] | None = None,
    parse_float: Callable[[str], Any] | None = None,
    parse_int: Callable[[str], Any] | None = None,
    parse_constant: Callable[[str], Any] | None = None,
    object_pairs_hook: Callable[[list[tuple[Any, Any]]], Any] | None = None,
    **kw: dict[str, Any],
) -> Any:
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
    cls: type[json.JSONDecoder] | None = None,
    object_hook: Callable[[dict[Any, Any]], Any] | None = None,
    parse_float: Callable[[str], Any] | None = None,
    parse_int: Callable[[str], Any] | None = None,
    parse_constant: Callable[[str], Any] | None = None,
    object_pairs_hook: Callable[[list[tuple[Any, Any]]], Any] | None = None,
    **kw: dict[str, Any],
) -> Any:
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


def dumps(
    obj: Any,
    *,
    skipkeys=False,
    ensure_ascii=True,
    check_circular=True,
    allow_nan=True,
    cls: type[JSONEncoder] | None = None,
    indent: int | None = None,
    separators: tuple[str, str] | None = None,
    default: Callable[[Any], Any] | None = None,
    sort_keys=False,
    trailing_comma=False,
    comments: Comments | None = None,
    **kw,
) -> str:
    """Serialize ``obj`` to a JSON formatted ``str``.

    Reference: ``json.dumps``
    """

    data = json.dumps(
        obj,
        skipkeys=skipkeys,
        ensure_ascii=ensure_ascii,
        check_circular=check_circular,
        allow_nan=allow_nan,
        cls=cls,
        indent=indent,
        separators=separators,
        default=default,
        sort_keys=sort_keys,
        **kw,
    )

    if trailing_comma:
        data = _add_trailing_comma(data)

    if comments is None:
        return data
    if indent is None:
        warnings.warn("Can't add comments to non-indented JSON", stacklevel=2)
        return data

    return _add_comments(data, comments)


def dump(
    obj: Any,
    fp: TextIO,
    *,
    skipkeys=False,
    ensure_ascii=True,
    check_circular=True,
    allow_nan=True,
    cls: type[JSONEncoder] | None = None,
    indent: int | None = None,
    separators: tuple[str, str] | None = None,
    default: Callable[[Any], Any] | None = None,
    sort_keys=False,
    trailing_comma=False,
    comments: Comments | None = None,
    **kw,
):
    """Serialize ``obj`` as a JSON formatted stream to ``fp`` (a
    ``.write()``-supporting file-like object).

    Reference: ``json.dump``
    """

    fp.write(
        dumps(
            obj,
            skipkeys=skipkeys,
            ensure_ascii=ensure_ascii,
            check_circular=check_circular,
            allow_nan=allow_nan,
            cls=cls,
            indent=indent,
            separators=separators,
            default=default,
            sort_keys=sort_keys,
            trailing_comma=trailing_comma,
            comments=comments,
            **kw,
        ),
    )
