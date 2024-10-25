import plotnine as p
from ..colors import get_color


def theme_udot(style="light", base_size=11, font_family="Arial", **kwargs):

    theme_colors = (
        kwargs["theme_colors"] if "theme_colors" in kwargs else _theme_colors[style]
    )

    half_size = base_size / 2

    line_size = kwargs["line_size"] if "line_size" in kwargs else base_size / 11
    half_line_size = line_size / 2

    strip_padding = kwargs["strip_padding"] if "strip_padding" in kwargs else 0.2

    udot_theme = p.theme_bw(base_size=base_size, base_family=font_family) + p.theme(
        text=p.element_text(color=get_color(theme_colors["text"])),
        strip_background=p.element_rect(
            fill=get_color(theme_colors["fill"]),
            color=get_color(theme_colors["text"]),
            size=half_line_size,
        ),
        strip_align=strip_padding,
        plot_background=p.element_rect(fill=get_color(theme_colors["background"])),
        panel_background=p.element_rect(fill=get_color(theme_colors["background"])),
        panel_border=p.element_rect(
            color=get_color(theme_colors["text"]), size=half_line_size
        ),
        panel_grid_major=p.element_line(
            color=get_color(theme_colors["lines"]), size=line_size
        ),
        panel_grid_minor=p.element_line(
            color=get_color(theme_colors["lines"]), size=half_line_size
        ),
        axis_ticks_major=p.element_line(
            color=get_color(theme_colors["text"]), size=half_line_size
        ),
        axis_ticks_minor=p.element_blank(),
        legend_background=p.element_rect(
            color=get_color(theme_colors["text"]),
            size=half_line_size,
            fill=get_color(theme_colors["background"]),
        ),
        legend_box_margin=half_size,
        legend_key=p.element_blank(),
    )
    return udot_theme


_theme_colors = {
    "light": {
        "text": "dark_blue",
        "fill": "light_gray",
        "lines": "light_gray",
        "background": "white",
    },
    "light_transparent": {
        "text": "dark_blue",
        "fill": "light_gray",
        "lines": "light_gray",
        "background": "#FFF0",
    },
    "dark": {
        "text": "light_gray",
        "fill": "dark_blue",
        "lines": "gray",
        "background": "dark_gray",
    },
    "dark_transparent": {
        "text": "light_gray",
        "fill": "dark_blue",
        "lines": "gray",
        "background": "#0000",
    },
}
