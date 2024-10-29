import os

if os.name == 'nt':
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    except Exception as e:
        print("Could not enable ANSI support:", e)

class ANSI:
    CSI = '\033['

    @staticmethod
    def color_code(code: int) -> str:
        """Returns a color code in the 8-bit (256) color space."""
        return f"{ANSI.CSI}38;5;{code}m"

    @staticmethod
    def rgb_color(r: int, g: int, b: int) -> str:
        """Returns an ANSI code for a 24-bit RGB color."""
        return f"{ANSI.CSI}38;2;{r};{g};{b}m"

    @staticmethod
    def background_code(code: int) -> str:
        """Returns a background color code in the 8-bit (256) color space."""
        return f"{ANSI.CSI}48;5;{code}m"

    @staticmethod
    def rgb_background(r: int, g: int, b: int) -> str:
        """Returns an ANSI code for a 24-bit RGB background color."""
        return f"{ANSI.CSI}48;2;{r};{g};{b}m"

    RESET = f"{CSI}0m"


class Colors:
    BASIC_COLORS = {
        'BLACK': 30, 'RED': 31, 'GREEN': 32, 'YELLOW': 33,
        'BLUE': 34, 'MAGENTA': 35, 'CYAN': 36, 'WHITE': 37,
        'LIGHT_BLACK': 90, 'LIGHT_RED': 91, 'LIGHT_GREEN': 92,
        'LIGHT_YELLOW': 93, 'LIGHT_BLUE': 94, 'LIGHT_MAGENTA': 95,
        'LIGHT_CYAN': 96, 'LIGHT_WHITE': 97
    }
    
    EXTENDED_COLORS = {
        'ORANGE': 208, 'BRIGHT_RED': 196, 'FOREST_GREEN': 34, 'DARK_GREEN': 22,
        'DARK_RED': 88, 'PEACH': 210, 'PASTEL_YELLOW': 228, 'PASTEL_GREEN': 120,
        'PASTEL_PURPLE': 141, 'BURNT_ORANGE': 130, 'ELECTRIC_BLUE': 45,
        'BRIGHT_PINK': 201, 'BRIGHT_ORANGE': 214, 'BRIGHT_TEAL': 51, 'OLIVE': 100,
        'DARK_SLATE': 235, 'SOFT_LAVENDER': 183, 'SOFT_PINK': 217,
        'LIGHT_SKY_BLUE': 153, 'PALE_MINT_GREEN': 121, 'GRAY_3': 237,
        'GRAY_7': 243, 'GRAY_11': 247, 'NEON_GREEN': 46, 'NEON_YELLOW': 226
    }

    def __getattr__(self, name: str) -> str:
        """Allow color retrieval with `Rcolor.COLOR_NAME`."""
        code = self.BASIC_COLORS.get(name.upper(), None) or self.EXTENDED_COLORS.get(name.upper(), None)
        return ANSI.color_code(code) if code else ANSI.RESET

    @classmethod
    def add_color(cls, name: str, code: int):
        """Add a new color to the extended color set."""
        cls.EXTENDED_COLORS[name.upper()] = code


class Backgrounds:
    BASIC_BACKGROUNDS = {
        'BLACK': 40, 'RED': 41, 'GREEN': 42, 'YELLOW': 43,
        'BLUE': 44, 'MAGENTA': 45, 'CYAN': 46, 'WHITE': 47,
        'LIGHT_BLACK': 100, 'LIGHT_RED': 101, 'LIGHT_GREEN': 102,
        'LIGHT_YELLOW': 103, 'LIGHT_BLUE': 104, 'LIGHT_MAGENTA': 105,
        'LIGHT_CYAN': 106, 'LIGHT_WHITE': 107
    }

    def __getattr__(self, name: str) -> str:
        """Allow background retrieval with `Rbackground.COLOR_NAME`."""
        code = self.BASIC_BACKGROUNDS.get(name.upper(), None)
        return ANSI.background_code(code) if code else ANSI.RESET


class Styles:
    STYLES = {
        'BOLD': f"{ANSI.CSI}1m", 'DIM': f"{ANSI.CSI}2m", 'ITALIC': f"{ANSI.CSI}3m",
        'UNDERLINE': f"{ANSI.CSI}4m", 'BLINK': f"{ANSI.CSI}5m", 'REVERSE': f"{ANSI.CSI}7m",
        'HIDDEN': f"{ANSI.CSI}8m", 'RESET': ANSI.RESET
    }

    def __getattr__(self, name: str) -> str:
        """Allow style retrieval with `Rstyle.STYLE_NAME`."""
        return self.STYLES.get(name.upper(), ANSI.RESET)

Rcolor = Colors()
Rbackground = Backgrounds()
Rstyle = Styles()


def color_text(text: str, color: str = "", background: str = "", style: str = "") -> str:
    """Applies color, background, and style to text."""
    return f"{color}{background}{style}{text}{Styles.RESET}"

"""
print(color_text("Hello in Red", Colors.get('RED')))
print(color_text("Hello with Peach Background", Colors.get('WHITE'), Backgrounds.get('PEACH')))
print(color_text("Bold Underlined", Colors.get('GREEN'), style=Styles.BOLD + Styles.UNDERLINE))

Colors.add_color('CUSTOM_BLUE', 27)
print(color_text("Custom Blue Text", Colors.get('CUSTOM_BLUE')))
"""
