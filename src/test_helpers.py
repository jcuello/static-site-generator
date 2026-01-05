import unittest
from helpers import split_nodes_delimiter
from textnode import TextNode, TextType

class TestHelpers(unittest.TestCase):
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
    self.assertEqual(len(new_nodes), 1)
    self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
    bold_node_count = len([node for node in new_nodes if node.text_type == TextType.BOLD])
    self.assertEqual(bold_node_count, 0)


if __name__ == "__main__":
  unittest.main()