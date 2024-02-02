from copy import deepcopy
from io import StringIO

import pytest

from jsonc import dump, dumps, load, loads


def test_loads():
    assert loads("{// comment \n}") == {}
    assert loads("{// comment \r}") == {}
    assert loads("{// comment \r\n}") == {}
    assert loads("{}// comment") == {}
    assert loads("{/* comment */}") == {}
    assert loads('{"spam": "ham // egg" /* comment */}') == {"spam": "ham // egg"}
    assert loads('{"spam": /* comment */"ham /* egg */"}') == {"spam": "ham /* egg */"}
    assert loads(r'"spam\"ham" // egg') == 'spam"ham'
    assert loads(r'"spam\"ham\\" // egg') == 'spam"ham\\'


def test_load():
    with open("tests/testfile.jsonc", encoding="utf-8") as f:
        load(f)


def test_dumps():
    assert dumps({}) == "{}"
    with pytest.warns(UserWarning):
        assert (
            dumps({"a": "b", "c": {}}, trailing_comma=True, comments="test")
            == '{"a": "b", "c": {},}'
        )
    assert dumps("{hello}", trailing_comma=True) == '"{hello}"'
    assert dumps({}, indent=2, comments="test") == "// test\n{}"
    with pytest.warns(UserWarning):
        assert dumps({}, indent=2, comments={"a": "b"}) == "{}"
    obj = {"a": {"b": "c"}, "d": [1, [2, 3], {"x": [6.7, [{}]]}]}
    comments = (
        "test2",
        {
            "a": ("nested dict", {"b": "nested key"}),
            "d": {
                0: "first array element",
                1: ("second element", {0: "first element of second element"}),
                2: (
                    "third element",
                    {"x": ("something", {1: "empty object/array test"})},
                ),
            },
        },
    )
    orig_comments = deepcopy(comments)

    expected = """
// test2
{
  // nested dict
  "a": {
    // nested key
    "b": "c"
  },
  "d": [
    // first array element
    1,
    // second element
    [
      // first element of second element
      2,
      3
    ],
    // third element
    {
      // something
      "x": [
        6.7,
        // empty object/array test
        [
          {}
        ]
      ]
    }
  ]
}
    """.strip()
    assert dumps(obj, indent=2, comments=comments) == expected
    assert comments == orig_comments
    assert (
        dumps(obj, indent=2, trailing_comma=True, comments=comments).count(",")
        - expected.count(",")
        == 7
    )


def test_dump():
    o = StringIO()
    dump([], o, indent=2, comments="test")
    assert o.getvalue() == "// test\n[]"
