from .elements import Element

class Text(Element):
    def render(self) -> str:
        style = self.css.get_style_string() if self.css else ""
        if self.centered:
            centering_style = "display: flex; justify-content: center; align-items: center;"
            style = f"{centering_style} {style}"
        return f'<textq style="{style}">{self.content}</textq>'