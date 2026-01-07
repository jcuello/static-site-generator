from textnode import BlockType, TextNode, TextType
import re

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
    return []

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

def extract_markdown_images(text:str) -> list[tuple[str, str]]:
  return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
  
def extract_markdown_links(text:str) -> list[tuple[str, str]]:
  return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes:list[TextNode]) -> list[TextNode]:
  if old_nodes == None:
    raise ValueError("old_nodes is required")
  
  new_nodes: list[TextNode] = []
  for node in old_nodes: # loop 1
    if node.text_type != TextType.TEXT:
      new_nodes.append(node)
    else:
      results: list[TextNode] = []
      markdown_images_info = extract_markdown_images(node.text)
      if len(markdown_images_info) == 0:
        new_nodes.append(node)
        continue # continues for loop 1

      node_text = node.text
      for image_alt, image_link in markdown_images_info: # loop 2
        sections = node_text.split(f"![{image_alt}]({image_link})", 1)
        before_target_text = sections[0]

        if before_target_text == '':
          break # breaks out of loop 2

        results.append(TextNode(before_target_text, TextType.TEXT))
        results.append(TextNode(image_alt, TextType.IMAGE, image_link))
        
        node_text = sections[1]

      # add any remaining text
      if len(node_text) > 0:
        results.append(TextNode(node_text, TextType.TEXT))

      new_nodes.extend(results)

  return new_nodes
  

def split_nodes_link(old_nodes:list[TextNode]) -> list[TextNode]:
  if old_nodes == None:
    raise ValueError("old_nodes is required")
  
  new_nodes: list[TextNode] = []
  for node in old_nodes: # loop 1
    if node.text_type != TextType.TEXT:
      new_nodes.append(node)
    else:
      results: list[TextNode] = []
      markdown_links_info = extract_markdown_links(node.text)
      if len(markdown_links_info) == 0:
        new_nodes.append(node)
        continue # continues for loop 1

      node_text = node.text
      for text_url, url in markdown_links_info: # loop 2
        sections = node_text.split(f"[{text_url}]({url})", 1)
        before_target_text = sections[0]

        if before_target_text == '':
          break # breaks out of loop 2

        results.append(TextNode(before_target_text, TextType.TEXT))
        results.append(TextNode(text_url, TextType.LINK, url))
        
        node_text = sections[1]

      # add any remaining text
      if len(node_text) > 0:
        results.append(TextNode(node_text, TextType.TEXT))

      new_nodes.extend(results)

  return new_nodes


def text_to_textnodes(text:str) -> list[TextNode]:
  text_node = TextNode(text, TextType.TEXT)
  new_nodes = split_nodes_delimiter([text_node], TextType.BOLD.delimiter, TextType.BOLD)
  new_nodes = split_nodes_delimiter(new_nodes, TextType.ITALIC.delimiter, TextType.ITALIC)
  new_nodes = split_nodes_delimiter(new_nodes, TextType.CODE.delimiter, TextType.CODE)
  new_nodes = split_nodes_image(new_nodes)
  new_nodes = split_nodes_link(new_nodes)
  return new_nodes

def markdown_to_blocks(markdown:str) -> list[str]:
  if markdown == None:
    raise ValueError("markdown is required")
  
  blocks = markdown.split("\n\n")
  result = []
  for block in blocks:
    block = block.strip()
    if block != '':
      result.append(block)

  return result

#TODO UNTESTED!! Need to write unit tests
def block_to_block_type(markdown_block:str) -> BlockType:
  if markdown_block == None:
    raise ValueError("markdown_block required")
  
  if markdown_block.startswith("#"):
    return BlockType.HEADING
  
  if markdown_block.startswith("```\n"):
    return BlockType.CODE
  
  if markdown_block.startswith("> "):
    return BlockType.QUOTE
  
  if markdown_block.startswith("- "):
    return BlockType.UNORDERED_LIST
  
  if markdown_block[0].isdigit() and markdown_block[:2] == "1.":
    lines = markdown_block.split("\n")
    # is it a list if it's only one line?
    if len(lines) > 1:
      previous_num = 1      
      for line in lines[1:]:
        parsed_num = re.findall(r'(^\d+\.)', line)
        if parsed_num == None or len(parsed_num) == 0:
          return BlockType.PARAGRAPH
        
        if int(parsed_num) != previous_num+1:
          return BlockType.PARAGRAPH
        previous_num = parsed_num
      
      return BlockType.ORDERED_LIST
  
  return BlockType.PARAGRAPH

