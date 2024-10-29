from .color import Rcolor, Rstyle, color_text

class Themes:
    @staticmethod
    def template(text, color, style=None):
        return color_text(text, color=color, style=style or Rstyle.BOLD)
    
    success = lambda text: Themes.template(text, Rcolor.GREEN)
    warning = lambda text: Themes.template(text, Rcolor.YELLOW, Rstyle.ITALIC)
    error = lambda text: Themes.template(text, Rcolor.RED)
    info = lambda text: Themes.template(text, Rcolor.CYAN)
