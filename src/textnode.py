from enum import Enum
from typing import Self

class TextType(Enum):
  TEXT = 1
  ITALIC = 2
  BOLD = 3
  CODE = 4
  LINK = 5
  IMAGE = 6


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