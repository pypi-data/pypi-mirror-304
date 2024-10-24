from .elements import Element

class NewLine(Element):
    def __init__(self):
        pass

    def render(self) -> str:
        return '<br>'