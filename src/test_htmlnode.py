import unittest
from htmlnode import HTMLNode

class TestHtmlNode(unittest.TestCase):
  link_node = HTMLNode(
    "a", "Boot.dev",
    [],
    {
      "href": "https://boot.dev",
      "target": "_blank"
    },
  )

  def test_props_to_html(self):
    props_html = TestHtmlNode.link_node.props_to_html()
    self.assertEqual(props_html, ' href="https://boot.dev" target="_blank"')

  def test_props_to_html_no_attributes(self):
    node = HTMLNode("p", "This is a paragraph tag with no attributes.")
    props_html = node.props_to_html()
    self.assertEqual(props_html, '')    

  def test_repr(self):
    repr_value = str(TestHtmlNode.link_node)
    self.assertEqual(
      repr_value, 
      "HTMLNode(a, Boot.dev, [], {'href': 'https://boot.dev', 'target': '_blank'})"
    )

if __name__ == "__main__":
  unittest.main()