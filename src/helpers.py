from textnode import TextNode, TextType
#from typing import Any

def split_nodes_delimiter(
    old_nodes:list[TextNode], delimiter:str, text_type:TextType
  ) -> list[TextNode]:
  new_nodes:list[TextNode] = []
  for node in old_nodes:
    if node.text_type != TextType.TEXT:
      new_nodes.append(node)
    else:
      new_nodes.extend(to_text_nodes(node.text, delimiter, text_type))
  
  return new_nodes

# checks to see if text is valid markdown with opening and closing delimiters
def to_text_nodes(text:str, delimiter:str, text_type:TextType) -> list[TextNode]:
  if delimiter == None:
    raise ValueError("delimiter is required")
  
  if text == None:
    raise ValueError("text is required")
  
  if len(text) == 0:
    return [TextNode("", TextType.TEXT)]

  delimiter_len = len(delimiter)
  delimiters_found = 0
  next_index = None
  results: list[TextNode] = []


  while True:
    start_index = text.find(delimiter)
    
    if start_index == -1:
      # append any remaining text for further processing if necessary
      if len(text) > 0:
        results.append(TextNode(text, TextType.TEXT))
      return results
        
    delimiters_found += 1
    next_index = text.find(delimiter, start_index+delimiter_len)
    
    if next_index == -1:
      break

    before_target_text = text[:start_index]
    # need to check length in case delimiter is at the beginning of the string
    if len(before_target_text) > 0:
      results.append(TextNode(before_target_text, TextType.TEXT))

    target_text = text[start_index+delimiter_len:next_index]
    results.append(TextNode(target_text, text_type))

    text = text[next_index+delimiter_len:]

  if delimiters_found % 2 != 0:
    raise Exception(f"Missing closing delimiter ({delimiter}) starting from index {start_index}")
  
  return results
