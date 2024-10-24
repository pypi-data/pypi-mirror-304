from .image import Image
from .elements import Element

class Body:
    def __init__(self):
        self.background = None
        self.elements = []

    def add(self, element: Element):
        self.elements.append(element)

    def setBackground(self, image: Image):
        self.background = image

    def render(self) -> str:
        bg_style = ""
        if self.background:
            if self.background.type == 'color':
                bg_style = f"background-color: {self.background.data};"
            else:
                bg_style = f"background-image: url(data:{self.background.type};base64,{self.background.data});"
        
        body_content = "".join([element.render() for element in self.elements])
        return f'<body style="{bg_style}">{body_content}</body>'