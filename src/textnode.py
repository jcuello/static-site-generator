from enum import Enum, auto
from typing import Self
import htmlnode

class TextType(Enum):
  TEXT = auto()
  BOLD = auto()
  ITALIC = auto()
  CODE = auto()
  LINK = auto()
  IMAGE = auto()

  @property
  def delimiter(self) -> str | None:
    match self.name:
      case "TEXT":
        return ""
      case "BOLD":
        return "**"
      case "ITALIC":
        return "_"
      case "CODE":
        return '`'
      case _:
        return None
      
class BlockType(Enum):
  PARAGRAPH = auto()
  HEADING = auto()
  CODE = auto()
  QUOTE = auto()
  UNORDERED_LIST = auto()
  ORDERED_LIST = auto()

# This will be used for the markdown input
class TextNode:
  def __init__(self, text:str, text_type:TextType, url:str=None):
    self.text = text
    self.text_type = text_type
    self.url = url

  def __eq__(self, rhs:Self):
    return (
      self.text == rhs.text and 
      self.text_type == rhs.text_type and
      self.url == rhs.url    
    )
  
  def __repr__(self:Self):
    return f"TextNode({self.text}, {self.text_type}, {self.url})"
  
def text_node_to_html_node(text_node:TextNode) -> htmlnode.HTMLNode:
  match text_node.text_type:
    case TextType.TEXT:
      return htmlnode.LeafNode(None, text_node.text)
    case TextType.BOLD:
      return htmlnode.LeafNode("b", text_node.text)
    case TextType.ITALIC:
      return htmlnode.LeafNode("i", text_node.text)
    case TextType.CODE:
      return htmlnode.LeafNode("code", text_node.text)
    case TextType.LINK:
      return htmlnode.LeafNode("a", text_node.text, {'href': text_node.url})
    case TextType.IMAGE:
      return htmlnode.LeafNode("img", "", {'src': text_node.url, 'alt': text_node.text})
    case _:
      raise ValueError(f"Invalid TextType: {text_node.text_type}")