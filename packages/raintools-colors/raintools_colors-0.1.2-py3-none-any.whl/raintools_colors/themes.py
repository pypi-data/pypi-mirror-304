from .color import Rcolor, Rstyle, color_text

class Themes:
    success = lambda text: color_text(text, color=Rcolor.GREEN, style=Rstyle.BOLD)
    warning = lambda text: color_text(text, color=Rcolor.YELLOW)
    error = lambda text: color_text(text, color=Rcolor.RED, style=Rstyle.BOLD)