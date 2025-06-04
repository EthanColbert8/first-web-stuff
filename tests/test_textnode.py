import unittest

from src.textnode import TextType, TextNode, textnode_to_html
from src.htmlnode import LeafNode

class TestTextNode(unittest.TestCase):
    def test_eq_plain(self):
        node1 = TextNode("Hello", TextType.BOLD)
        node2 = TextNode("Hello", TextType.BOLD)

        self.assertEqual(node1, node2)
    
    def test_neq_content(self):
        node1 = TextNode("Hello", TextType.BOLD)
        node2 = TextNode("Goodbye", TextType.BOLD)

        self.assertNotEqual(node1, node2)
    
    def test_neq_type(self):
        node1 = TextNode("Hello", TextType.BOLD)
        node2 = TextNode("Hello", TextType.TEXT)

        self.assertNotEqual(node1, node2)
    
    def test_eq_link(self):
        node1 = TextNode("Link", TextType.LINK, "https://example.com")
        node2 = TextNode("Link", TextType.LINK, "https://example.com")

        self.assertEqual(node1, node2)
    
    def test_neq_url(self):
        node1 = TextNode("Link", TextType.LINK, "https://example.com")
        node2 = TextNode("Link", TextType.LINK, "https://another.com")

        self.assertNotEqual(node1, node2)

class TestTextNodeConverter(unittest.TestCase):
    def test_conversion_text(self):
        text = TextNode("Hello, world!", TextType.TEXT)
        html_node = textnode_to_html(text)
        
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "Hello, world!")
    
    def test_conversion_bold(self):
        text = TextNode("Bold text", TextType.BOLD)
        html_node = textnode_to_html(text)
        
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")
    
    def test_conversion_italic(self):
        text = TextNode("Italic text", TextType.ITALIC)
        html_node = textnode_to_html(text)
        
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")
    
    def test_conversion_code(self):
        text = TextNode("Code snippet", TextType.CODE)
        html_node = textnode_to_html(text)
        
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "Code snippet")
    
    def test_conversion_link(self):
        text = TextNode("Example link", TextType.LINK, "https://example.com")
        html_node = textnode_to_html(text)
        
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Example link")
        self.assertEqual(html_node.props, {"href": "https://example.com"})
    
    def test_conversion_image(self):
        text = TextNode("Example image", TextType.IMAGE, "https://example.com/image.png")
        html_node = textnode_to_html(text)
        
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://example.com/image.png", "alt": "Example image"})
    
    def test_conversion_unknown(self):
        text = TextNode("Mystery text!", TextType.TEXT)
        text.text_type = "NORMAL" # fake a bad value
        with self.assertRaisesRegex(ValueError, r"Unknown text type: NORMAL"):
            html_node = textnode_to_html(text)

if (__name__ == "__main__"):
    unittest.main()