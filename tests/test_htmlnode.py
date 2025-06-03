import unittest

from src.htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_repr_null(self):
        node = HTMLNode()
        expected = "HTMLNode()"
        self.assertEqual(repr(node), expected)
    
    def test_repr_tag_value(self):
        node = HTMLNode("div", "Example content.")
        expected = "HTMLNode(tag=\"div\", value=\"Example content.\")"
        self.assertEqual(repr(node), expected)
    
    # really should test it with children, but that's way too much work lmao

    def test_repr_props(self):
        node = HTMLNode("div", "Example content.", props={"class": "example", "id": "test"})
        expected = "HTMLNode(tag=\"div\", value=\"Example content.\", props={\"class\": \"example\", \"id\": \"test\"})"
        self.assertEqual(repr(node), expected)
    
    def test_props_to_html_empty(self):
        node = HTMLNode("div", "Example content.")
        expected = ""
        self.assertEqual(node.props_to_html(), expected)
    
    def test_props_to_html(self):
        node = HTMLNode("div", "Example content.", props={"class": "example", "id": "test"})
        expected = " class=\"example\" id=\"test\""
        self.assertEqual(node.props_to_html(), expected)

if (__name__ == "__main__"):
    unittest.main()