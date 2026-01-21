from htmlnode import HTMLNode, ParentNode
from textnode import BlockType, TextNode, TextType, text_node_to_html_node
import re
import os

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

        # nothing else to process
        if before_target_text == '':
          node_text = ""
          results.append(TextNode(image_alt, TextType.IMAGE, image_link))
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

        # nothing else to process
        if before_target_text == '':
          node_text = ""
          results.append(TextNode(text_url, TextType.LINK, url))
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

def block_to_block_type(markdown_block:str) -> BlockType:
  if markdown_block == None:
    raise ValueError("markdown_block required")
  
  heading_match:re.Match[str] = re.match(r"(^#+ )", markdown_block)
  if heading_match != None:
    return BlockType.HEADING
  
  lines: list[str] = []
  for line in markdown_block.split(os.linesep):
    if line.strip() != '':
      lines.append(line)    

  lines_len = len(lines)
  if lines_len > 1 and lines[0].startswith("```") and lines[-1].rstrip().endswith("```"):    
    return BlockType.CODE
  
  quote_lines = [line for line in lines if line.startswith("> ")]
  if len(quote_lines) == lines_len:
    return BlockType.QUOTE
  
  unordered_lines = [line for line in lines if line.startswith("- ")]
  if len(unordered_lines) == lines_len:
    return BlockType.UNORDERED_LIST
  
  if lines[0][:2] == "1.":
    # is it a list if it's only one item?
    if len(lines) > 1:
      previous_num:int = 1      
      for line in lines[1:]:
        num_match = re.findall(r'(^\d+\. )', line)
        if len(num_match) == 0:
          return BlockType.PARAGRAPH
        
        parsed_num = int(float(num_match[0]))
        if parsed_num != previous_num+1:
          return BlockType.PARAGRAPH
        
        previous_num = parsed_num
      
      return BlockType.ORDERED_LIST
  
  return BlockType.PARAGRAPH

def block_to_html_node(markdown_block:str) -> HTMLNode:
  block_type = block_to_block_type(markdown_block)
  text_nodes = text_to_textnodes(markdown_block)  
  html_nodes = [text_node_to_html_node(node) for node in text_nodes]
  match block_type:
    case BlockType.HEADING:
      heading_size = min(6, len(markdown_block.split(" ", maxsplit=1)[0]))
      html_nodes[0].value = html_nodes[0].value.replace("#", "").lstrip()
      return ParentNode(f"h{heading_size}", html_nodes)
    
    case BlockType.CODE:
      markdown_block = markdown_block.lstrip(f"```{os.linesep}").rstrip("```")
      code_node_child = text_node_to_html_node(TextNode(markdown_block, TextType.TEXT))
      return ParentNode("pre", [ParentNode("code", [code_node_child])])
    
    case BlockType.QUOTE:
      for node in html_nodes:
        node.value = node.value.replace("> ", "").replace(os.linesep, " ")
      return ParentNode("blockquote", html_nodes)
    
    # Lists need special handling before sending it to text_to_textnodes since
    # each node is a separate line, can't parse the whole text with newlines everywhere
    case BlockType.UNORDERED_LIST:
      # Need to group these per li
      text_nodes: list[list[TextNode]] = [] 
      for line in markdown_block.split(os.linesep):
        line = line.lstrip("- ")
        line_nodes = text_to_textnodes(line)
        text_nodes.append(line_nodes)
      
      li_nodes: list[ParentNode] = []
      for li_text_node in text_nodes:
        li_nodes.append(ParentNode("li", [text_node_to_html_node(text_node) for text_node in li_text_node]))

      return ParentNode("ul", li_nodes)
    
    case BlockType.ORDERED_LIST:
      text_nodes: list[list[TextNode]] = [] 
      for line in markdown_block.split(os.linesep):
        line = re.sub(r'(^\d+\.) ', "", line, count=1)
        line_nodes = text_to_textnodes(line)
        text_nodes.append(line_nodes)

      li_nodes: list[ParentNode] = []
      for li_text_node in text_nodes:
        li_nodes.append(ParentNode("li", [text_node_to_html_node(text_node) for text_node in li_text_node]))

      return ParentNode("ol", li_nodes)      
      
    case _:
      def remove_newlines(node:HTMLNode):
        node.value = node.value.replace(os.linesep, " ") if node != None else None
        return node
      return ParentNode("p", list(map(remove_newlines, html_nodes)))

def markdown_to_html_node(markdown:str) -> HTMLNode:
  blocks = markdown_to_blocks(markdown)

  if blocks == []:
    return ParentNode("div", [])
  
  root_children: list[HTMLNode] = []
  for block in blocks:
    root_children.append(block_to_html_node(block))
  
  return ParentNode("div", root_children)
