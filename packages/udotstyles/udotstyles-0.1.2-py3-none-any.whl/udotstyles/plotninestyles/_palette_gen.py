from ..colors.colors import get_color
from ..colors.palettes import get_palette_qual, get_palette_seq, get_palette_div


def _palette_gen_qual(
    palette="main",
    reverse=False,
    # backward=False,
):
    def f(n):
        if n > len(get_palette_qual(palette)):
            raise Exception(
                "Not enough colors in this palette!\n"
                + 'Number of colors in palette "'
                + palette
                + '": '
                + str(len(get_palette_qual(palette)))
                + "\n"
                + "Number of colors asked for: "
                + str(n)
            )

        colors = get_palette_qual(palette)
        # if backward:
        #     colors.reverse()
        pal = colors[:n]
        if reverse:
            pal.reverse()
        return pal

    return f


def _palette_gen_seq(palette=None, colorlist=None, reverse=False):
    if palette is not None and colorlist is not None:
        raise UserWarning(
            "Both `palette` and `colorlist` specified. Will use `colorlist`."
        )

    if colorlist is None:
        if palette is None:
            raise ValueError("Specify one of `palette` or `colorlist`")
        else:
            colorlist = get_palette_seq(palette)
            if reverse:
                colorlist.reverse()
            colordict = {"colors": colorlist, "values": None}
            return colordict

    if reverse:
        colorlist.reverse()

    if any([type(x) is tuple for x in colorlist]):
        if any([type(x) is not tuple for x in colorlist]):
            raise ValueError("Cannot mix tuples and non-tuples in `colorlist`")
        else:
            colors, values = zip(*colorlist)
            colordict = {"colors": get_color(*colors), "values": list(values)}
    else:
        colordict = {"colors": get_color(*colorlist), "values": None}

    return colordict


def _palette_gen_div(palette=None, colors=None, reverse=False):

    if palette is not None and colors is not None:
        raise UserWarning("Both `palette` and `colors` specified. Will use `colors`.")

    if colors is None:
        if palette is None:
            raise ValueError("Specify one of `palette` or `colors`")
        else:
            colors = get_palette_div(palette)

    if type(colors) is not dict:
        if len(colors) == 3:
            colors = {
                "low": get_color(colors[0]),
                "mid": get_color(colors[1]),
                "high": get_color(colors[2]),
            }
        elif len(colors) == 2:
            colors = {
                "low": get_color(colors[0]),
                "mid": get_color("white"),
                "high": get_color(colors[1]),
            }
        else:
            raise ValueError(
                "`colors` should be a dict or an iteratable of length 2 or 3"
            )
    else:
        colors = {k: get_color(v) for k, v in colors.items()}

    if reverse:
        colors["low"], colors["high"] = colors["high"], colors["low"]

    return colors
