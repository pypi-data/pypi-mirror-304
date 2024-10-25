import pprint
import copy

colors_dict = {
    "primary": {
        "lightblue": "#5A87C6",
        "orange": "#E86924",
        "darkblue": "#0B2444",
    },
    "secondary": {
        "lightgreen": "#ABC746",
        "mustard": "#F5A31B",
        "mediumblue": "#09549C",
        "tan": "#C7A25A",
        "turquoise": "#55CCD4",
        "red": "#E8261A",  # Only use to highlight something strong or negative
    },
    "tertiary": {
        "redrock": "#C7776D",
        "brown": "#7A5B1F",
        "tacao": "#F7AA74",
        "purple": "#8A52A1",
        "darkgreen": "#6B7A31",
        "yellow": "#DED843",
    },
    "grays": {
        "black": "#000000",
        "darkgray": "#454545",
        "gray": "#888888",
        "lightgray": "#EEEEEE",
        "white": "#FFFFFF",
    },
}

_colors_list = (
    colors_dict["primary"]
    | colors_dict["secondary"]
    | colors_dict["tertiary"]
    | colors_dict["grays"]
)


def get_color(*cols):
    """Get color(s) from the UDOT color palette

    Args:
        cols: The colors to get

    Returns:
        Either a list of hex colors, or a single hex color.
        If a given color does not exist in the UDOT color palette,
        that color will be returned as-is.
    """
    cols = _process_input_cols(*cols)
    if len(cols) < 1:
        raise ValueError("Specify one or more colors")

    cols = [_get_color_from_dict_if_exists(col) for col in cols]

    # If only one color is requested, return a string instead of a list
    if len(cols) == 1:
        cols = cols[0]

    return cols


def list_colors(*cols) -> None:
    """List colors from the UDOT color dictionary (or list the whole dictionary)

    Args:
        cols: The colors to get

    Returns:
        None
    """

    # Add the message about "red" to the "red" entry
    colors_dict_red_msg = copy.deepcopy(colors_dict)
    colors_dict_red_msg["secondary"]["red"] = (
        colors_dict_red_msg["secondary"]["red"]
        + " (Only use red to highlight something strong or negative)"
    )

    colors_list_red_msg = copy.deepcopy(_colors_list)
    colors_list_red_msg["red"] = (
        colors_list_red_msg["red"]
        + " (Only use red to highlight something strong or negative)"
    )

    cols = _process_input_cols(*cols)

    # If no arguments given, print the whole dictionary, otherwise print specific colors
    if len(cols) < 1:
        pprint.pprint(colors_dict_red_msg, sort_dicts=False)
    else:
        for c in cols:
            c = _sanitize_color_name(c)
            print(c + ":" + " " + colors_list_red_msg[c])

    return None


def _sanitize_color_name(col):
    """Fix different spellings of colors etc.

    Args:
        col: The color name to sanitize

    Returns:
        str: The sanitized color name if a string, or the color unchanged if not a string
    """
    if type(col) != str:
        return col

    col = col.lower().replace("grey", "gray").replace("_", "")
    col = "mediumblue" if col == "blue" else col
    col = "darkgreen" if col == "green" else col
    return col


def _get_color_from_dict_if_exists(col: str) -> str:
    """Get a color by name from the UDOT color dictionary if it exists,
    otherwise return the color as-is

    Args:
        col (str): The color to get

    Returns:
        str: Either the hex color from the UDOT color dictionary (if it exists),
        or the color as-is
    """
    if _sanitize_color_name(col) in _colors_list.keys():
        return _colors_list[_sanitize_color_name(col)]
    else:
        return col


def _process_input_cols(*cols):
    if len(cols) < 1:
        return []

    if len(cols) > 1:
        for col in cols:
            if type(col) == list:
                raise ValueError("If a list is used, it must be the only argument")

    # If a list is given, use the list directly
    if type(cols[0]) == list:
        cols = cols[0]

    return cols
