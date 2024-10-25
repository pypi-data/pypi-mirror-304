import pytest

from udotstyles import colors
from udotstyles.colors.colors import _sanitize_color_name, colors_dict

import pprint
import copy


def test_get_color_single():
    assert colors.get_color("mediumblue") == "#09549C"


def test_get_color_multiple():
    assert colors.get_color("mediumblue", "red") == ["#09549C", "#E8261A"]


def test_get_color_list():
    assert colors.get_color(["mediumblue", "red"]) == ["#09549C", "#E8261A"]


def test_get_color_list_and_other():
    with pytest.raises(ValueError) as excinfo:
        colors.get_color(["mediumblue", "red"], "orange")
    assert str(excinfo.value) == "If a list is used, it must be the only argument"
    with pytest.raises(ValueError) as excinfo:
        colors.get_color("orange", ["mediumblue", "red"])
    assert str(excinfo.value) == "If a list is used, it must be the only argument"


def test_get_no_colors():
    with pytest.raises(ValueError) as excinfo:
        colors.get_color()
    assert str(excinfo.value) == "Specify one or more colors"


def test_sanitize_color_name():
    assert _sanitize_color_name("MediumBlue") == "mediumblue"
    assert _sanitize_color_name("grey") == "gray"
    assert _sanitize_color_name("mediumgrey") == "mediumgray"
    assert _sanitize_color_name("light_blue") == "lightblue"
    assert _sanitize_color_name("blue") == "mediumblue"
    assert _sanitize_color_name("green") == "darkgreen"


def test_only_convert_udot_colors():
    assert colors.get_color("gold") == "gold"


def test_only_sanitize_udot_colors():
    assert colors.get_color("slategrey") == "slategrey"


def test_sanitization_pass_non_strings():
    assert _sanitize_color_name((0.5, 0.5, 0.5)) == (0.5, 0.5, 0.5)


def test_list_single_color(capfd):
    colors.list_colors("blue")
    out, err = capfd.readouterr()
    assert out == "mediumblue: #09549C\n"

    colors.list_colors(["blue"])
    out, err = capfd.readouterr()
    assert out == "mediumblue: #09549C\n"


def test_list_multiple_colors(capfd):
    colors.list_colors("blue", "red")
    out, err = capfd.readouterr()
    assert (
        out
        == "mediumblue: #09549C\n"
        + "red: #E8261A (Only use red to highlight something strong or negative)\n"
    )

    colors.list_colors(["blue", "red"])
    out, err = capfd.readouterr()
    assert (
        out
        == "mediumblue: #09549C\n"
        + "red: #E8261A (Only use red to highlight something strong or negative)\n"
    )


def test_list_all_colors(capfd):
    colors.list_colors()
    out, err = capfd.readouterr()

    colors_dict_red_msg = copy.deepcopy(colors_dict)
    colors_dict_red_msg["secondary"]["red"] = (
        colors_dict_red_msg["secondary"]["red"]
        + " (Only use red to highlight something strong or negative)"
    )

    should_be = pprint.pformat(colors_dict_red_msg, sort_dicts=False) + "\n"

    assert out == should_be


def test_list_bad_color(capfd):
    with pytest.raises(KeyError) as excinfo:
        colors.list_colors("gold")
    assert str(excinfo.value) == "'gold'"
