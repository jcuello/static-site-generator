import unittest

from textnode import TextNode, TextType, text_node_to_html_node

class TestTextNode(unittest.TestCase):
  def test_eq(self):
    node = TextNode("This is a text node", TextType.BOLD)
    node2 = TextNode("This is a text node", TextType.BOLD)
    self.assertEqual(node, node2)

  def test_not_eq(self):
    node = TextNode("This is a bold text node", TextType.BOLD)
    node2 = TextNode("This is a italic text node", TextType.ITALIC)
    self.assertNotEqual(node, node2)

  def test_link_default_value(self):
    node = TextNode("This is a URL", TextType.LINK)
    self.assertEqual(node.url, None)
    
  def test_text(self):
    node = TextNode("This is a text node", TextType.TEXT)
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, None)
    self.assertEqual(html_node.value, "This is a text node")

  def test_text(self):
    node = TextNode("This is a text node", TextType.TEXT)
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, None)
    self.assertEqual(html_node.value, "This is a text node")

  def test_bold(self):
    node = TextNode("This is a BOLD text node", TextType.BOLD)
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, "b")
    self.assertEqual(html_node.value, "This is a BOLD text node")

  def test_italic(self):
    node = TextNode("This is a ITALIC text node", TextType.ITALIC)
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, "i")
    self.assertEqual(html_node.value, "This is a ITALIC text node")

  def test_code(self):
    node = TextNode("This is a CODE text node", TextType.CODE)
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, "code")
    self.assertEqual(html_node.value, "This is a CODE text node")

  def test_link(self):
    node = TextNode("This is a LINK text node", TextType.LINK, "https://www.google.com")
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, "a")
    self.assertEqual(html_node.props["href"], "https://www.google.com")
    self.assertEqual(html_node.value, "This is a LINK text node")

  def test_image(self):
    node = TextNode("This is a IMAGE text node", TextType.IMAGE, "https://www.google.com/image.jpg")
    html_node = text_node_to_html_node(node)
    self.assertEqual(html_node.tag, "img")
    self.assertEqual(html_node.props["src"], "https://www.google.com/image.jpg")
    self.assertEqual(html_node.props["alt"], "This is a IMAGE text node")
    self.assertEqual(html_node.value, "")

if __name__ == "__main__":
  unittest.main()