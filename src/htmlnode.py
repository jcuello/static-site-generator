from typing import Self

class HTMLNode:
  def __init__(
      self, tag:str | None=None, value:str | None=None, 
      children:list[Self] | None=None, 
      props:dict[str, str] | None=None):
    self.tag = tag
    self.value = value
    self.children = children
    self.props = props

  # Subclasses will override this
  def to_html(self):
    raise NotImplementedError()
  
  def props_to_html(self:Self):
    if self.props == None or len(self.props) == 0:
      return ""
    
    kvp_list = []
    for k,v in self.props.items():
      kvp_list.append(f'{k}="{v}"')
    return " " + " ".join(kvp_list)
  
  def __repr__(self:Self):
    return (
      f'HTMLNode(' +
      f'{self.tag}, ' + 
      f'{self.value}, ' +
      f'{self.children}, ' +
      f'{self.props})'
    )

class LeafNode(HTMLNode):
  # When tag is None, it will just be raw text
  def __init__(
      self, tag:str | None, value:str, 
      props:dict[str, str] | None=None
    ):
    super().__init__(tag, value, None, props)

  def to_html(self):
    if self.value == None:
      raise ValueError("Node must have a value")
    
    if self.tag == None:
      return self.value
    
    return (
      f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
    )