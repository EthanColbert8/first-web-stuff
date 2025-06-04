from enum import Enum
from .htmlnode import LeafNode

class TextType(Enum):
    TEXT = 1
    BOLD = 2
    ITALIC = 3
    CODE = 4
    LINK = 5
    IMAGE = 6

class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str = None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, TextNode):
            return False
        return (self.text == other.text and self.text_type == other.text_type and self.url == other.url)
    
    def __repr__(self) -> str:
        return f"TextNode(\"{self.text}\", TextType.{self.text_type.name}, \"{self.url}\")"

def textnode_to_html(text: TextNode) -> LeafNode:
    match text.text_type:
        case TextType.TEXT:
            return LeafNode(None, text.text)
        case TextType.BOLD:
            return LeafNode("b", text.text)
        case TextType.ITALIC:
            return LeafNode("i", text.text)
        case TextType.CODE:
            return LeafNode("code", text.text)
        case TextType.LINK:
            return LeafNode("a", text.text, {"href": text.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text.url, "alt": text.text})
        case _:
            raise ValueError(f"Unknown text type: {text.text_type}")