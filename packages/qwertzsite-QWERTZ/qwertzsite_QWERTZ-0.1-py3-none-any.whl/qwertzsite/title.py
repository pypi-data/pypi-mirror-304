from .text import Text

class Title(Text):
    def render(self) -> str:
        style = self.css.get_style_string() if self.css else ""
        if self.centered:
            centering_style = "text-align: center;"
            style = f"{centering_style} {style}"
        return f'<h1 style="{style}">{self.content}</h1>'