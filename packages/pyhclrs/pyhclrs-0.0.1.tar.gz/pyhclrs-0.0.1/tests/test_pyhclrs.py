import pytest
import pyhclrs


def test_basic():
    assert pyhclrs.loads('variable "test" {}') == {"variable": {"test": {}}}


def test_parse_error():
    with pytest.raises(pyhclrs.HCLError):
        pyhclrs.loads('variable "test {}')


def test_empty_list():
    out = pyhclrs.loads("""variable "test" { default = [] }""")
    assert out["variable"]["test"]["default"] == []


def test_null():
    out = pyhclrs.loads("""variable "test" { default = null }""")
    assert out["variable"]["test"]["default"] is None