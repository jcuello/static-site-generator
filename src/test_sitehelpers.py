import unittest

from helpers import markdown_to_html_node
from sitehelpers import (
  extract_title
)

class TestSiteHelpers(unittest.TestCase):
  def test_extract_title(self):
    title = extract_title("# Hello")
    self.assertEqual(title, "Hello")

if __name__ == "__main__":
  unittest.main()