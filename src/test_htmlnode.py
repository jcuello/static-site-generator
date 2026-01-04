import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

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

class TestLeafNode(unittest.TestCase):
  def test_leaf_to_html_p(self):
    node = LeafNode("p", "Hello, world!")
    self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

  def test_leaf_to_html_a_with_attributes(self):
    node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
    self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

class TestParentNode(unittest.TestCase):
  def test_to_html_with_children(self):
    child_node = LeafNode("span", "child")
    parent_node = ParentNode("div", [child_node])
    self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

  def test_to_html_with_grandchildren(self):
    grandchild_node = LeafNode("b", "grandchild")
    child_node = ParentNode("span", [grandchild_node])
    parent_node = ParentNode("div", [child_node])
    self.assertEqual(
        parent_node.to_html(),
        "<div><span><b>grandchild</b></span></div>",
    )

  def test_to_html_with_empty_nested_parent(self):    
    child_node = ParentNode("span", [])
    parent_node = ParentNode("div", [child_node])
    self.assertEqual(
        parent_node.to_html(),
        "<div><span></span></div>",
    )

  def test_to_html_with_children_and_props(self):
    child_node = LeafNode("a", "Google.com", {"href": "https://www.google.com", "target":"_blank"})
    parent_node = ParentNode("div", [child_node])
    self.assertEqual(parent_node.to_html(), '<div><a href="https://www.google.com" target="_blank">Google.com</a></div>')

if __name__ == "__main__":
  unittest.main()