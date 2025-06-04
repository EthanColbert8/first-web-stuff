import unittest

from src.htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_repr_null(self):
        node = HTMLNode()
        expected = "HTMLNode()"
        self.assertEqual(repr(node), expected)
    
    def test_repr_tag_value(self):
        node = HTMLNode("div", "Example content.")
        expected = "HTMLNode(tag=\"div\", value=\"Example content.\")"
        self.assertEqual(repr(node), expected)
    
    # should test with children, but that's too much work lmao

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
    
class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_empty(self):
        node = LeafNode("p", "")
        expected = "<p></p>"
        self.assertEqual(node.to_html(), expected)
    
    def test_leaf_to_html(self):
        node = LeafNode("p", "Hello, world!")
        expected = "<p>Hello, world!</p>"
        self.assertEqual(node.to_html(), expected)

    def test_leaf_to_html_notag(self):
        node = LeafNode(None, "Just plain-ass text")
        expected = "Just plain-ass text"
        self.assertEqual(node.to_html(), expected)
    
    def test_leaf_to_html_notag_props(self):
        node = LeafNode(None, "Some random text.", {"class": "example", "id": "test"})
        expected = "Some random text."
        self.assertEqual(node.to_html(), expected)
    
    def test_leaf_to_html_props(self):
        node = LeafNode("a", "Some random text.", {"href": "not_a_website"})
        expected = "<a href=\"not_a_website\">Some random text.</a>"
        self.assertEqual(node.to_html(), expected)

class TestParentNode(unittest.TestCase):
    def test_parent_to_html_onelevel(self):
        child_nodes = [
            LeafNode("h2", "This is a header"),
            LeafNode("p", "Here's some body text.")
        ]

        node = ParentNode("div", child_nodes)
        expected = "<div><h2>This is a header</h2><p>Here's some body text.</p></div>"

        self.assertEqual(node.to_html(), expected)
    
    def test_parent_to_html_notag(self):
        child_nodes = [
            LeafNode(None, "Plain text here. "),
            LeafNode("b", "Bolded text here,"),
            LeafNode(None, "more plain text.")
        ]

        node = ParentNode("p", child_nodes)
        expected = "<p>Plain text here. <b>Bolded text here,</b>more plain text.</p>"

        self.assertEqual(node.to_html(), expected)
    
    def test_parent_to_html_empty(self):
        node = ParentNode("div", [])
        expected = "<div></div>"
        self.assertEqual(node.to_html(), expected)
    
    def test_parent_to_html_empty_props(self):
        node = ParentNode("div", [], props={"class": "example", "id": "test"})
        expected = "<div class=\"example\" id=\"test\"></div>"
        self.assertEqual(node.to_html(), expected)
    
    def test_parent_to_html_deep(self):
        grandchild_nodes = [
            LeafNode("p", "Some paragraph text."),
            LeafNode("p", "Some more paragraph text.")
        ]
        child_nodes = [
            ParentNode("section", grandchild_nodes)
        ]

        node = ParentNode("div", child_nodes, props={"class": "container"})
        expected = "<div class=\"container\"><section><p>Some paragraph text.</p><p>Some more paragraph text.</p></section></div>"

        self.assertEqual(node.to_html(), expected)
    
    def test_parent_to_html_deep_mixed(self):
        grandchild_nodes = [
            LeafNode("p", "Some paragraph text."),
            LeafNode("p", "Some more paragraph text.", props={"id": "test"})
        ]
        child_nodes = [
            ParentNode("section", grandchild_nodes, props={"class": "section"}),
            LeafNode("footer", "Footer content")
        ]

        node = ParentNode("div", child_nodes)
        expected = "<div><section class=\"section\"><p>Some paragraph text.</p><p id=\"test\">Some more paragraph text.</p></section><footer>Footer content</footer></div>"

        self.assertEqual(node.to_html(), expected)
    
    def test_parent_to_html_list(self):
        list_items = [
            LeafNode("li", "Item 1"),
            LeafNode("li", "Item 2"),
            LeafNode("li", "Item 3")
        ]
        child_nodes = [
            LeafNode(None, "Pre-list text: "),
            ParentNode("ul", list_items),
            LeafNode(None, " Post-list text.")
        ]

        node = ParentNode("p", child_nodes)
        expected = "<p>Pre-list text: <ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul> Post-list text.</p>"
        
        self.assertEqual(node.to_html(), expected)
    
    def test_parent_to_html_notag(self):
        child_nodes = [
            LeafNode("p", "This is a paragraph.")
        ]

        node = ParentNode("div", child_nodes)
        node.tag = None # simulate a bad value

        with self.assertRaisesRegex(ValueError, r"Parent nodes must have a tag\."):
            node.to_html()
    
    def test_parent_to_html_nochildren(self):
        child_nodes = [
            LeafNode("p", "This is a paragraph.")
        ]

        node = ParentNode("div", child_nodes)
        node.children = None # simulate a bad value

        with self.assertRaisesRegex(ValueError, r"Parent nodes must have children\."):
            node.to_html()
    
if (__name__ == "__main__"):
    unittest.main()