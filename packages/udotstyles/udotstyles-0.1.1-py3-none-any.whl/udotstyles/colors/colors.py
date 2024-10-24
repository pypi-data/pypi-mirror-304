import pprint

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

    # If a list is given, use the list directly
    if type(cols[0]) == list:
        cols = cols[0]

    cols = [_sanitize_color_name(c) for c in cols]
    cols = [_get_color_from_dict_if_exists(col) for col in cols]

    # If only one color is requested, return a string instead of a list
    if len(cols) == 1:
        cols = cols[0]

    return cols


def list_colors(*cols) -> None:
    """List colors from the UDOT color dictionary (or the whole dictionary)

    Args:
        cols: The colors to get

    Returns:
        None
    """

    # Add the message about "red" to the "red" entry
    colors_dict_red_msg = colors_dict.copy()
    colors_dict_red_msg["secondary"]["red"] = (
        colors_dict_red_msg["secondary"]["red"]
        + " (Only use red to highlight something strong or negative)"
    )

    # If no arguments given, print the whole dictionary, otherwise print specific colors
    if len(cols) < 1:
        pprint.pprint(colors_dict_red_msg)
    else:
        # Add the message about "red" to the "red" entry
        colors_list_red_msg = _colors_list.copy()
        colors_list_red_msg["red"] = (
            colors_list_red_msg["red"]
            + " (Only use red to highlight something strong or negative)"
        )
        # If a list is given, use the list directly
        if type(cols[0]) == list:
            cols = cols[0]
        for c in cols:
            c = _sanitize_color_name(c)
            print(c + ":" + " " + colors_list_red_msg[c])

    return None


def _sanitize_color_name(col: str) -> str:
    """Fix different spellings of colors etc.

    Args:
        col (str): The color name to sanitize

    Returns:
        str: The sanitized color name
    """
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
    if col in _colors_list.keys():
        return _colors_list[col]
    else:
        return col
