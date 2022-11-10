from jsonc import __version__, load, loads

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
