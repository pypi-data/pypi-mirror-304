import os
import sys

class ColorText:
    CSI = '\033['

    COLORS = {
        "black": f"{CSI}30m",
        "red": f"{CSI}31m",
        "green": f"{CSI}32m",
        "yellow": f"{CSI}33m",
        "blue": f"{CSI}34m",
        "magenta": f"{CSI}35m",
        "cyan": f"{CSI}36m",
        "white": f"{CSI}37m",
        "light_black": f"{CSI}90m",
        "light_red": f"{CSI}91m",
        "light_green": f"{CSI}92m",
        "light_yellow": f"{CSI}93m",
        "light_blue": f"{CSI}94m",
        "light_magenta": f"{CSI}95m",
        "light_cyan": f"{CSI}96m",
        "light_white": f"{CSI}97m",
        "orange": f"{CSI}38;5;208m",
        "bright_red": f"{CSI}38;5;196m",
        "forest_green": f"{CSI}38;5;34m",
        "dark_green": f"{CSI}38;5;22m",
        "dark_red": f"{CSI}38;5;88m",
        "peach": f"{CSI}38;5;210m",
        "pastel_yellow": f"{CSI}38;5;228m",
        "pastel_green": f"{CSI}38;5;120m",
        "pastel_purple": f"{CSI}38;5;141m",
        "burnt_orange": f"{CSI}38;5;130m",
        "electric_blue": f"{CSI}38;5;45m",
        "bright_pink": f"{CSI}38;5;201m",
        "bright_orange": f"{CSI}38;5;214m",
        "bright_teal": f"{CSI}38;5;51m",
        "olive": f"{CSI}38;5;100m",
        "dark_slate": f"{CSI}38;5;235m",
        "soft_lavender": f"{CSI}38;5;183m",
        "soft_pink": f"{CSI}38;5;217m",
        "light_sky_blue": f"{CSI}38;5;153m",
        "pale_mint_green": f"{CSI}38;5;121m",
        "gray_3": f"{CSI}38;5;237m",
        "gray_7": f"{CSI}38;5;243m",
        "gray_11": f"{CSI}38;5;247m",
        "neon_green": f"{CSI}38;5;46m",
        "neon_yellow": f"{CSI}38;5;226m",
        "reset": f"{CSI}0m"
    }

    STYLES = {
        "bold": f"{CSI}1m",
        "dim": f"{CSI}2m",
        "italic": f"{CSI}3m",
        "underline": f"{CSI}4m",
        "blink": f"{CSI}5m",
        "reverse": f"{CSI}7m",
        "hidden": f"{CSI}8m",
        "reset": f"{CSI}0m"
    }

    def __init__(self):
        if os.name == 'nt':
            try:
                import ctypes
                kernel32 = ctypes.windll.kernel32
                kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
            except Exception as e:
                print("Could not enable ANSI support:", e)

    def __getattr__(self, name):
        """Dynamically return ANSI code for colors and styles with case-insensitivity."""
        normalized_name = name.lower()
        
        if normalized_name in self.COLORS:
            return self.COLORS[normalized_name]
        elif normalized_name in self.STYLES:
            return self.STYLES[normalized_name]
        else:
            raise AttributeError(f"'ColorText' object has no attribute '{name}'")

    def color_by_code(self, code: int) -> str:
        """
        Returns the ANSI color escape sequence for a 256-color code.
        Args:
            code (int): An integer between 0 and 255 representing an ANSI 256 color code.
        """
        if 0 <= code <= 255:
            return f"{self.CSI}38;5;{code}m"
        else:
            raise ValueError("Color code must be between 0 and 255.")

    def reset(self):
        """Return the reset code to clear styles and colors."""
        return self.COLORS["reset"]

    @property
    def reset_color(self):
        """Return the ANSI reset code for formatting."""
        return self.COLORS["reset"]

