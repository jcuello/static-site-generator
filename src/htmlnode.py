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
