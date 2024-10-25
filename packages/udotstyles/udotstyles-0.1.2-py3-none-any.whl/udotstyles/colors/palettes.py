from .colors import get_color
import pprint


palettes = {
    "qualitative": {
        "main": [
            "light_blue",
            "orange",
            "dark_blue",
            "gray",
            "medium_blue",
            "light_green",
            "dark_gray",
            "turquoise",
            "tacao",
            "brown",
        ],
        "alt": [],
        "grayscale": [],
        "highlight": [],
    },
    "sequential": {
        "blue": ["darkblue", "white"],
    },
    "diverging": {
        "blueorange": ["blue", "orange"],
    },
}


def list_palettes(pal_type=None):
    if pal_type is not None:
        try:
            print(pal_type + ":")
            pprint.pprint(palettes[pal_type], sort_dicts=False)
        except KeyError:
            raise KeyError(
                "`pal_type` should be one of `qualitative`, `sequential`, `diverging`"
            )
    else:
        pprint.pprint(palettes, sort_dicts=False)
    return None


def show_palettes(pal_type="qualitative", palette=None):
    # TODO: Create this function
    return None


def get_palette(pal_type="qualitative", palette="main", hex=True):
    palette = _sanitize_palette_name(palette)
    pal = palettes[pal_type][palette]
    if hex:
        pal = get_color(pal)
    return pal


def get_palette_qual(palette="main"):
    return get_palette(pal_type="qualitative", palette=palette, hex=True)


def get_palette_seq(palette="blue"):
    return get_palette(pal_type="sequential", palette=palette, hex=True)


def get_palette_div(palette="blueorange"):
    return get_palette(pal_type="diverging", palette=palette, hex=True)


def _sanitize_palette_name(pal: str) -> str:
    pal = pal.lower().replace("grey", "gray").replace("_", "")
    return pal
