from pathlib import Path

import pytest

import jsonc


def test_unused():
    with pytest.warns(UserWarning, match="Unused comment with key: warn") as w:
        jsonc.dumps({}, indent=2, comments={"warn": "spam"})
        assert Path(w.list[0].filename).absolute() == Path(__file__).absolute()
