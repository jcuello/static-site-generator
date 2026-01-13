import unittest
from helpers import (
  split_nodes_delimiter, extract_markdown_images, extract_markdown_links,
  split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_blocks,
  block_to_block_type
)
from textnode import BlockType, TextNode, TextType

class TestHelpers(unittest.TestCase):
  # split_nodes_delimiter tests
  def test_split_nodes_delimiter_with_valid_markdown(self):
    text_node = TextNode("First node **bold node** third node", TextType.TEXT)
    new_nodes = split_nodes_delimiter([text_node], "**", TextType.BOLD)
    self.assertEqual(len(new_nodes), 3)
    bold_node_count = len([node for node in new_nodes if node.text_type == TextType.BOLD])
    self.assertEqual(bold_node_count, 1)

  def test_split_nodes_delimiter_with_invalid_markdown(self):
    text_node = TextNode("First node *bold node** third node", TextType.TEXT)
    with self.assertRaises(Exception):
      split_nodes_delimiter([text_node], "**", TextType.BOLD)    

  def test_split_nodes_delimiter_without_annotations_text(self):
    text_node = TextNode("Plain old text", TextType.TEXT)
    new_nodes = split_nodes_delimiter([text_node], "**", TextType.BOLD)
    text_node_count = len([node for node in new_nodes if node.text_type == TextType.TEXT])
    self.assertEqual(len(new_nodes), 1)
    self.assertEqual(text_node_count, 1)

  def test_split_nodes_delimiter_with_multiple_annotations(self):
    text_node = TextNode(
      "First node `code node` **bold node** third node " +
      "_italic node_ and _another italic_", 
      TextType.TEXT
    )

    # 1 BOLD, 2 TEXT
    new_nodes = split_nodes_delimiter([text_node], "**", TextType.BOLD)
    #print(new_nodes)
    self.assertEqual(len(new_nodes), 3)
    bold_node_count = len([node for node in new_nodes if node.text_type == TextType.BOLD])
    self.assertEqual(bold_node_count, 1)

    # 1 BOLD, 1 CODE, 3 TEXT 
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    #print(new_nodes)
    self.assertEqual(len(new_nodes), 5)
    code_node_count = len([node for node in new_nodes if node.text_type == TextType.CODE])
    self.assertEqual(code_node_count, 1)

    # 1 BOLD, 1 CODE, 2 ITALIC, 4 TEXT 
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
    #print(new_nodes)
    self.assertEqual(len(new_nodes), 8)    
    italic_node_count = len([node for node in new_nodes if node.text_type == TextType.ITALIC])
    self.assertEqual(italic_node_count, 2)

  def test_split_nodes_delimiter_empty_string(self):
    text_node = TextNode("", TextType.TEXT)
    new_nodes = split_nodes_delimiter([text_node], "**", TextType.BOLD)
    self.assertEqual(len(new_nodes), 0)
    bold_node_count = len([node for node in new_nodes if node.text_type == TextType.BOLD])
    self.assertEqual(bold_node_count, 0)

  # extract_markdown_images tests
  def test_extract_markdown_images(self):
    text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
    expected_result = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
    actual_result = extract_markdown_images(text)
    #print(actual_result)
    self.assertListEqual(actual_result, expected_result)


  # extract_markdown_links tests
  def test_extract_markdown_links(self):
    text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    expected_result = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
    actual_result = extract_markdown_links(text)
    self.assertListEqual(actual_result, expected_result)

  # images tests
  def test_split_image(self):
    node = TextNode(
      "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
      TextType.TEXT,
    )
    new_nodes = split_nodes_image([node])
    self.assertListEqual(
      [
        TextNode("This is text with an ", TextType.TEXT),
        TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
        TextNode(" and another ", TextType.TEXT),
        TextNode(
          "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
        ),
      ],
      new_nodes,
    )

  def test_split_image_with_no_images(self):
    node = TextNode(
      "This is plain text. **This text is bold.** _And this is italic!_",
      TextType.TEXT,
    )
    new_nodes = split_nodes_image([node])
    self.assertListEqual(
      [
        TextNode(
          "This is plain text. **This text is bold.** _And this is italic!_", 
          TextType.TEXT
        ),
      ],
      new_nodes,
    )

  # links tests
  def test_split_link(self):
    node = TextNode(
      "This is text with a [link](https://google.com) and another [second link](https://boot.dev)",
      TextType.TEXT,
    )
    new_nodes = split_nodes_link([node])
    self.assertListEqual(
      [
        TextNode("This is text with a ", TextType.TEXT),
        TextNode("link", TextType.LINK, "https://google.com"),
        TextNode(" and another ", TextType.TEXT),
        TextNode(
          "second link", TextType.LINK, "https://boot.dev"
        ),
      ],
      new_nodes,
    )

  def test_split_link_with_no_links(self):
    node = TextNode(
      "This is plain text. **This text is bold.** _And this is italic!_",
      TextType.TEXT,
    )
    new_nodes = split_nodes_link([node])
    self.assertListEqual(
      [
        TextNode(
          "This is plain text. **This text is bold.** _And this is italic!_", 
          TextType.TEXT
        ),
      ],
      new_nodes,
    )

  # text_to_textnodes tests
  def test_text_to_textnodes(self):
    self.maxDiff = 1_000
    text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    new_nodes = text_to_textnodes(text)
    self.assertListEqual(
      [
        TextNode("This is ", TextType.TEXT),
        TextNode("text", TextType.BOLD),
        TextNode(" with an ", TextType.TEXT),
        TextNode("italic", TextType.ITALIC),
        TextNode(" word and a ", TextType.TEXT),
        TextNode("code block", TextType.CODE),
        TextNode(" and an ", TextType.TEXT),
        TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
        TextNode(" and a ", TextType.TEXT),
        TextNode("link", TextType.LINK, "https://boot.dev"),
      ],
      new_nodes,
    )

  def test_markdown_to_blocks(self):
    md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
    blocks = markdown_to_blocks(md)
    self.assertEqual(
        blocks,
        [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ],
    )

  def test_block_to_block_type(self):    
    heading_block ="# This is heading 1 block"
    code_block = """```
This is a code block.


This is the second line in the block.


And this is the third  ```  
"""
    quote_block="""
> This is a quote block
> This is the second line in the block
> And the third
"""
    unordered_block = """
- This is item one
- This is item two
- This is item three
"""
    ordered_block = """
1. Item 1
2. Item 2
3. Item 3
"""
    paragraph_block = """
Paragraph block, the next line should
not make it something else.
"""
    self.assertEqual(block_to_block_type(heading_block), BlockType.HEADING)
    self.assertEqual(block_to_block_type(code_block), BlockType.CODE)
    self.assertEqual(block_to_block_type(quote_block), BlockType.QUOTE)
    self.assertEqual(block_to_block_type(unordered_block), BlockType.UNORDERED_LIST)
    self.assertEqual(block_to_block_type(ordered_block), BlockType.ORDERED_LIST)
    self.assertEqual(block_to_block_type(paragraph_block), BlockType.PARAGRAPH)
if __name__ == "__main__":
  unittest.main()