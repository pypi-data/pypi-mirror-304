import os

if os.name == 'nt':
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    except Exception as e:
        print("Could not enable ANSI support:", e)

class Rcolor:
    CSI = '\033['

    BLACK = f"{CSI}30m"
    RED = f"{CSI}31m"
    GREEN = f"{CSI}32m"
    YELLOW = f"{CSI}33m"
    BLUE = f"{CSI}34m"
    MAGENTA = f"{CSI}35m"
    CYAN = f"{CSI}36m"
    WHITE = f"{CSI}37m"
    LIGHT_BLACK = f"{CSI}90m"
    LIGHT_RED = f"{CSI}91m"
    LIGHT_GREEN = f"{CSI}92m"
    LIGHT_YELLOW = f"{CSI}93m"
    LIGHT_BLUE = f"{CSI}94m"
    LIGHT_MAGENTA = f"{CSI}95m"
    LIGHT_CYAN = f"{CSI}96m"
    LIGHT_WHITE = f"{CSI}97m"
    ORANGE = f"{CSI}38;5;208m"
    BRIGHT_RED = f"{CSI}38;5;196m"
    FOREST_GREEN = f"{CSI}38;5;34m"
    DARK_GREEN = f"{CSI}38;5;22m"
    DARK_RED = f"{CSI}38;5;88m"
    PEACH = f"{CSI}38;5;210m"
    PASTEL_YELLOW = f"{CSI}38;5;228m"
    PASTEL_GREEN = f"{CSI}38;5;120m"
    PASTEL_PURPLE = f"{CSI}38;5;141m"
    BURNT_ORANGE = f"{CSI}38;5;130m"
    ELECTRIC_BLUE = f"{CSI}38;5;45m"
    BRIGHT_PINK = f"{CSI}38;5;201m"
    BRIGHT_ORANGE = f"{CSI}38;5;214m"
    BRIGHT_TEAL = f"{CSI}38;5;51m"
    OLIVE = f"{CSI}38;5;100m"
    DARK_SLATE = f"{CSI}38;5;235m"
    SOFT_LAVENDER = f"{CSI}38;5;183m"
    SOFT_PINK = f"{CSI}38;5;217m"
    LIGHT_SKY_BLUE = f"{CSI}38;5;153m"
    PALE_MINT_GREEN = f"{CSI}38;5;121m"
    GRAY_3 = f"{CSI}38;5;237m"
    GRAY_7 = f"{CSI}38;5;243m"
    GRAY_11 = f"{CSI}38;5;247m"
    NEON_GREEN = f"{CSI}38;5;46m"
    NEON_YELLOW = f"{CSI}38;5;226m"
    RESET = f"{CSI}0m"


class Rbackground:
    CSI = '\033['

    BLACK = f"{CSI}40m"
    RED = f"{CSI}41m"
    GREEN = f"{CSI}42m"
    YELLOW = f"{CSI}43m"
    BLUE = f"{CSI}44m"
    MAGENTA = f"{CSI}45m"
    CYAN = f"{CSI}46m"
    WHITE = f"{CSI}47m"
    LIGHT_BLACK = f"{CSI}100m"
    LIGHT_RED = f"{CSI}101m"
    LIGHT_GREEN = f"{CSI}102m"
    LIGHT_YELLOW = f"{CSI}103m"
    LIGHT_BLUE = f"{CSI}104m"
    LIGHT_MAGENTA = f"{CSI}105m"
    LIGHT_CYAN = f"{CSI}106m"
    LIGHT_WHITE = f"{CSI}107m"
    RESET = f"{CSI}0m"


class Rstyle:
    CSI = '\033['

    BOLD = f"{CSI}1m"
    DIM = f"{CSI}2m"
    ITALIC = f"{CSI}3m"
    UNDERLINE = f"{CSI}4m"
    BLINK = f"{CSI}5m"
    REVERSE = f"{CSI}7m"
    HIDDEN = f"{CSI}8m"
    RESET = f"{CSI}0m"


def color_text(text: str, color: str = "", background: str = "", style: str = "") -> str:
    """Combines color, background, and style into a formatted string."""
    return f"{color}{background}{style}{text}{Rstyle.RESET}{Rcolor.RESET}{Rbackground.RESET}"

""""
formatter = TextFormatter().color(Rcolor.blue).background(Rbackground.yellow).style(Rstyle.UNDERLINE)
print(formatter.apply("Hello, World!"))

print(Themes.success("Operation successful!"))
print(Themes.warning("Warning: Proceed with caution."))
print(Themes.error("Error: Action failed!"))

import time
for i in range(101):
    progress_bar(i, 100)
    time.sleep(0.05)

print(f"{blend_rgb((255, 0, 0), (0, 255, 0), 0.5)}Blended Color Text{Rstyle.RESET}")
"""