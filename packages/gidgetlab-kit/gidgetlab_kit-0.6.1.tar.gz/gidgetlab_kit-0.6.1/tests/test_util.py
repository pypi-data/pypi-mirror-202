import pytest
from gidgetlab_kit import util


@pytest.mark.parametrize(
    "input, params",
    [
        ([], {}),
        (("a=b", "c=d", "e=f"), {"a": "b", "c": "d", "e": "f"}),
        (("archived=true",), {"archived": "true"}),
        (
            ("order_by=updated_at", "visibility=private"),
            {"order_by": "updated_at", "visibility": "private"},
        ),
    ],
)
def test_convert_params_to_dict(input, params):
    assert util.convert_params_to_dict(input) == params


@pytest.mark.parametrize("input", [("foo",), ("a=b", "archived")])
def test_convert_params_to_dict_failed(input):
    with pytest.raises(ValueError) as e:
        util.convert_params_to_dict(input)
    assert "shall be separated by '='" in str(e)
