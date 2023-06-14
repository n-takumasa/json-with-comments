from jsonc import __version__, load, loads, dump, dumps
from io import StringIO

try:
    import tomllib  # type: ignore
except ImportError:
    import tomli as tomllib  # type: ignore


def test_version():
    with open("pyproject.toml", "rb") as f:
        version = tomllib.load(f)["tool"]["poetry"]["version"]
        assert __version__ == version


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
    with open("tests/testfile.jsonc", "r", encoding="utf-8") as f:
        load(f)


def test_dumps():
    assert dumps({}) == "{}"
    assert (
        dumps({"a": "b", "c": {}}, trailing_comma=True, comments="test")
        == '{"a": "b", "c": {},}'
    )
    assert dumps({}, indent=2, comments="test") == "// test\n{}"
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
    assert (
        dumps(obj, indent=2, trailing_comma=True, comments=comments).count(",")
        - expected.count(",")
        == 7
    )


def test_dump():
    o = StringIO()
    dump([], o, indent=2, comments="test")
    assert o.getvalue() == "// test\n[]"
