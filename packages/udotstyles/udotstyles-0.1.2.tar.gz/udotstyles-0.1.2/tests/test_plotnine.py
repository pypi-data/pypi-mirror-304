# %%
import os

os.chdir("..")

from udotstyles.plotninestyles import scales as us
from udotstyles.plotninestyles import themes as ut
from plotnine import *
from plotnine.data import mtcars
import pandas as pd
from udotstyles.colors import get_color

# %%
mtcars = mtcars.assign(cyl=pd.Categorical(mtcars.cyl))

# %%
(
    ggplot(mtcars, aes(x="hp", y="mpg", color="cyl"))
    + geom_point()
    + us.scale_color_udot(reverse=True)
)
# %%
(
    ggplot(mtcars, aes(x="hp", y="cyl", color="mpg"))
    + geom_jitter()
    + us.scale_color_udot_seq(palette="blue", reverse=True)
)

# %%
(
    ggplot(mtcars, aes(x="hp", y="cyl", color="mpg"))
    + geom_jitter()
    + us.scale_color_udot_seq(colorlist=["blue", "tacao"], reverse=True)
)

# %%
(
    ggplot(mtcars, aes(x="hp", y="cyl", color="mpg"))
    + geom_jitter()
    + us.scale_color_udot_seq(colorlist=["blue", "#000000"], reverse=False)
)

# %%
p = (
    ggplot(mtcars, aes(x="hp", y="mpg", color="cyl", size="gear"))
    + facet_grid("gear", "carb")
    + geom_point()
    + us.scale_color_udot()
)
p2 = (
    ggplot(mtcars, aes(x="hp", y="mpg", color="cyl", size="gear"))
    + geom_point()
    + us.scale_color_udot()
)

# %%
p2 + ut.theme_udot("dark")

# %%
