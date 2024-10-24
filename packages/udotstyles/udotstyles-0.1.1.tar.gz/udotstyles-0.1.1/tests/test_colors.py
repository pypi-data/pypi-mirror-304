# %%
import os

os.chdir("..")

from udotstyles import colors

#### Colors ####
# %%
print(colors.get_color("blue"))
print(colors.get_color("blue", "red"))
print(colors.get_color(["blue", "red"]))

# %%
colors.list_colors()
colors.list_colors("blue")
colors.list_colors("blue", "red")
colors.list_colors(["blue", "red"])


#### Palettes ####
# %%
colors.list_palettes()
colors.list_palettes("qualitative")

# %%
colors.get_palette()
