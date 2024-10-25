import pytest

from udotstyles.colors import palettes

import pprint


def test_list_one_palette_type(capfd):
    palettes.list_palettes("qualitative")
    out, err = capfd.readouterr()

    should_be = (
        "qualitative:\n"
        + pprint.pformat(palettes.palettes["qualitative"], sort_dicts=False)
        + "\n"
    )

    assert out == should_be


def test_list_all_palettes(capfd):
    palettes.list_palettes()
    out, err = capfd.readouterr()

    should_be = pprint.pformat(palettes.palettes, sort_dicts=False) + "\n"

    assert out == should_be


def test_list_bad_palette_type():
    with pytest.raises(KeyError) as excinfo:
        palettes.list_palettes("bad_palette_type")
    assert (
        str(excinfo.value)
        == "'`pal_type` should be one of `qualitative`, `sequential`, `diverging`'"
    )
