from .color import Rcolor, Rstyle, Rbackground

class TextFormatter:
    def __init__(self):
        self.styles = []
        
    def apply(self, text: str) -> str:
        style_code = "".join(set(self.styles))  # avoid duplicates
        return f"{style_code}{text}{Rstyle.RESET}{Rcolor.RESET}{Rbackground.RESET}"
    
    def color(self, color: str) -> 'TextFormatter':
        self.styles.append(color)
        return self
    
    def background(self, background: str) -> 'TextFormatter':
        self.styles.append(background)
        return self
    
    def style(self, style: str) -> 'TextFormatter':
        self.styles.append(style)
        return self
    
    def reset(self) -> 'TextFormatter':
        """Resets the current style settings."""
        self.styles.clear()
        return self
    
def color_contrast(fg, bg):
    """Adjusts foreground color for readability against the background."""
    fg_luminance = 0.2126*fg[0] + 0.7152*fg[1] + 0.0722*fg[2]
    bg_luminance = 0.2126*bg[0] + 0.7152*bg[1] + 0.0722*bg[2]
    return fg if abs(fg_luminance - bg_luminance) > 50 else invert_color(fg)
    
def gradient_text(text, start_color, end_color):
    """Apply a gradient effect over the text from start_color to end_color."""
    gradient_ratio = [i / (len(text) - 1) for i in range(len(text))]
    gradient = [blend_rgb(start_color, end_color, ratio) for ratio in gradient_ratio]
    return ''.join(f"{color}{char}" for color, char in zip(gradient, text)) + Rstyle.RESET

def progress_bar(progress, total, length=40):
    """Displays a progress bar in the terminal."""
    percent = progress / total
    filled_length = int(length * percent)
    bar = "█" * filled_length + '-' * (length - filled_length)
    print(f'\rProgress: |{bar}| {int(percent * 100)}%', end='\r')
    if progress == total:
        print()


def rgb_color(r: int, g: int, b: int) -> str:
    """Returns a 24-bit RGB foreground color ANSI code."""
    return f"\033[38;2;{r};{g};{b}m"


def rgb_background(r: int, g: int, b: int) -> str:
    """Returns a 24-bit RGB background color ANSI code."""
    return f"\033[48;2;{r};{g};{b}m"


def blend_rgb(color1: tuple, color2: tuple, ratio: float) -> str:
    """Blends two RGB colors by a ratio and returns the ANSI color code."""
    r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
    g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
    b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
    return rgb_color(r, g, b)

def invert_color(color: tuple) -> str:
    """Return the inverted color of an RGB color."""
    r, g, b = 255 - color[0], 255 - color[1], 255 - color[2]
    return rgb_color(r, g, b)

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