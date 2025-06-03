import unittest

from src.textnode import TextType, TextNode

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
        node2 = TextNode("Hello", TextType.NORMAL)

        self.assertNotEqual(node1, node2)
    
    def test_eq_link(self):
        node1 = TextNode("Link", TextType.LINK, "https://example.com")
        node2 = TextNode("Link", TextType.LINK, "https://example.com")

        self.assertEqual(node1, node2)
    
    def test_neq_url(self):
        node1 = TextNode("Link", TextType.LINK, "https://example.com")
        node2 = TextNode("Link", TextType.LINK, "https://another.com")

        self.assertNotEqual(node1, node2)


if (__name__ == "__main__"):
    unittest.main()