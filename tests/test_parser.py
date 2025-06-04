import unittest

from src.parser import split_nodes_delimiter
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

if (__name__ == "__main__"):
    unittest.main()