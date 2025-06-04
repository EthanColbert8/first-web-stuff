import unittest

from src.parser import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_images, split_nodes_links
from src.textnode import TextNode, TextType

def AssertEqualLists(testcase, list1, list2):
    '''
    Helper function to check equality of lists in test cases.
    '''
    testcase.assertEqual(len(list1), len(list2), "Lists are of different lengths.")

    for item1, item2 in zip(list1, list2):
        testcase.assertEqual(item1, item2)

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_text_only(self):
        nodes = [
            TextNode("Hello, world!", TextType.TEXT),
            TextNode("This is a test.", TextType.TEXT)
        ]

        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)

        expected = [
            TextNode("Hello, world!", TextType.TEXT),
            TextNode("This is a test.", TextType.TEXT)
        ]

        AssertEqualLists(self, result, expected)
    
    def test_split_bold(self):
        nodes = [
            TextNode("Hello, **world**!", TextType.TEXT),
            TextNode("This **is** a test.", TextType.TEXT)
        ]

        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)

        expected = [
            TextNode("Hello, ", TextType.TEXT),
            TextNode("world", TextType.BOLD),
            TextNode("!", TextType.TEXT),
            TextNode("This ", TextType.TEXT),
            TextNode("is", TextType.BOLD),
            TextNode(" a test.", TextType.TEXT)
        ]

        AssertEqualLists(self, result, expected)
    
    def test_split_italic(self):
        nodes = [
            TextNode("Hello, _world_!", TextType.TEXT),
            TextNode("This _is_ a test.", TextType.TEXT)
        ]

        result = split_nodes_delimiter(nodes, "_", TextType.ITALIC)

        expected = [
            TextNode("Hello, ", TextType.TEXT),
            TextNode("world", TextType.ITALIC),
            TextNode("!", TextType.TEXT),
            TextNode("This ", TextType.TEXT),
            TextNode("is", TextType.ITALIC),
            TextNode(" a test.", TextType.TEXT)
        ]

        AssertEqualLists(self, result, expected)
    
    def test_split_code(self):
        nodes = [
            TextNode("`Hello`, world!", TextType.TEXT),
            TextNode("This `is` a test.", TextType.TEXT)
        ]

        result = split_nodes_delimiter(nodes, "`", TextType.CODE)

        expected = [
            TextNode("Hello", TextType.CODE),
            TextNode(", world!", TextType.TEXT),
            TextNode("This ", TextType.TEXT),
            TextNode("is", TextType.CODE),
            TextNode(" a test.", TextType.TEXT)
        ]

        AssertEqualLists(self, result, expected)
    
    def test_split_unmatched_delimiter(self):
        nodes = [
            TextNode("Hello, **world!", TextType.TEXT),
            TextNode("This is a test.", TextType.TEXT)
        ]

        with self.assertRaises(ValueError):
            split_nodes_delimiter(nodes, "**", TextType.BOLD)

class TestLinksImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "Here is an image: ![alt text](image_url.jpg)"
        result = extract_markdown_images(text)
        expected = [("alt text", "image_url.jpg")]
        AssertEqualLists(self, result, expected)

    def test_extract_markdown_links(self):
        text = "Here is a link: [link text](http://example.com)"
        result = extract_markdown_links(text)
        expected = [("link text", "http://example.com")]
        AssertEqualLists(self, result, expected)
    
    def test_extract_markdown_links_multiple(self):
        text = "Here is a link: [link1](http://example1.com) and another [link2](http://example2.com)"
        result = extract_markdown_links(text)
        expected = [
            ("link1", "http://example1.com"),
            ("link2", "http://example2.com")
        ]
        AssertEqualLists(self, result, expected)
    
    def test_extract_markdown_images_multiple(self):
        text = "Here is an image: ![alt1](image1.jpg) and another ![alt2](image2.png)"
        result = extract_markdown_images(text)
        expected = [
            ("alt1", "image1.jpg"),
            ("alt2", "image2.png")
        ]
        AssertEqualLists(self, result, expected)
    
    def test_extract_markdown_links_no_match(self):
        text = "This text has no links."
        result = extract_markdown_links(text)
        expected = []
        AssertEqualLists(self, result, expected)

    def test_extract_markdown_images_no_match(self):
        text = "This text has no images."
        result = extract_markdown_images(text)
        expected = []
        AssertEqualLists(self, result, expected)
    
    def test_extract_markdown_images_mixed_content(self):
        text = "There's an image ![alt text](image_url.jpg) and a link [link text](https://example.com) in this one."
        result = extract_markdown_images(text)
        expected = [("alt text", "image_url.jpg")]
        AssertEqualLists(self, result, expected)
    
    def test_extract_markdown_links_mixed_content(self):
        text = "There's an image ![alt text](image_url.jpg) and a link [link text](https://example.com) in this one."
        result = extract_markdown_links(text)
        expected = [("link text", "https://example.com")]
        AssertEqualLists(self, result, expected)

class TestSplitNodesImagesLinks(unittest.TestCase):
    def test_split_nodes_images(self):
        nodes = [
            TextNode("Here is an image: ![alt text](image_url.jpg)", TextType.TEXT),
            TextNode("This is a test.", TextType.TEXT)
        ]

        result = split_nodes_images(nodes)

        expected = [
            TextNode("Here is an image: ", TextType.TEXT),
            TextNode("alt text", TextType.IMAGE, "image_url.jpg"),
            TextNode("This is a test.", TextType.TEXT)
        ]

        AssertEqualLists(self, result, expected)

    def test_split_nodes_links(self):
        nodes = [
            TextNode("Here is a link: [link text](http://example.com) and some text after.", TextType.TEXT),
            TextNode("This is a test.", TextType.TEXT)
        ]

        result = split_nodes_links(nodes)

        expected = [
            TextNode("Here is a link: ", TextType.TEXT),
            TextNode("link text", TextType.LINK, "http://example.com"),
            TextNode(" and some text after.", TextType.TEXT),
            TextNode("This is a test.", TextType.TEXT)
        ]

        AssertEqualLists(self, result, expected)

if (__name__ == "__main__"):
    unittest.main()