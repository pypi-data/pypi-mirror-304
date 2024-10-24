from dataclasses import dataclass
from typing import Optional
from .elements import Element
import base64

@dataclass
class Image:
    data: str
    type: str
    alt: str = ""
    width: Optional[int] = None
    height: Optional[int] = None

    @classmethod
    def fromHex(cls, hex_color: str, width: Optional[int] = None, height: Optional[int] = None):
        if not hex_color.startswith('#'):
            hex_color = f'#{hex_color}'
        # Create a 1x1 pixel SVG with the specified color
        svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="1" height="1"><rect width="1" height="1" fill="{hex_color}"/></svg>'
        encoded_svg = base64.b64encode(svg.encode('utf-8')).decode('utf-8')
        return cls(data=encoded_svg, type='image/svg+xml', width=width, height=height)

    @classmethod
    def fromFile(cls, file_path: str, alt: str = "", width: Optional[int] = None, height: Optional[int] = None):
        with open(file_path, 'rb') as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        file_extension = file_path.split('.')[-1].lower()
        return cls(data=encoded_string, type=f'image/{file_extension}', alt=alt, width=width, height=height)

    def render(self) -> str:
        size_attrs = ""
        if self.width:
            size_attrs += f' width="{self.width}"'
        if self.height:
            size_attrs += f' height="{self.height}"'
        return f'<img src="data:{self.type};base64,{self.data}" alt="{self.alt}"{size_attrs} style="object-fit: cover;">'

class ImageElement(Element):
    def __init__(self, image: Image):
        super().__init__("")
        self.image = image
        self.width = None
        self.height = None

    def setWidth(self, width: int):
        self.width = width
        return self
    
    def setHeight(self, height: int):
        self.height = height
        return self

    def render(self) -> str:
        style = self.css.get_style_string() if self.css else ""
        if self.centered:
            centering_style = "display: flex; justify-content: center; align-items: center;"
            style = f"{centering_style} {style}"

        size_attrs = ""
        if self.width:
            size_attrs += f' width="{self.width}"'
        if self.height:
            size_attrs += f' height="{self.height}"'

        img_html = self.image.render()
        if size_attrs:
            # Replace the existing width and height attributes
            img_html = img_html.replace('>', f'{size_attrs}>')

        return f'<div style="{style}">{img_html}</div>'