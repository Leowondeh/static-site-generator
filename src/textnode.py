from enum import Enum

class TextType(Enum):
    NORMAL = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, target):
        text_equal = self.text == target.text
        type_equal = self.text_type == target.text_type
        url_equal = self.url == target.url

        return text_equal and type_equal and url_equal
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"