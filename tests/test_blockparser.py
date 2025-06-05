import unittest

from src.blockparser import BlockType, markdown_to_blocks, block_to_blocktype

def AssertEqualLists(testcase, list1, list2):
    '''
    Helper function to check equality of lists in test cases.
    '''
    testcase.assertEqual(len(list1), len(list2), "Lists are of different lengths.")

    for item1, item2 in zip(list1, list2):
        testcase.assertEqual(item1, item2)

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks_normal(self):
        markdown = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        expected = [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ]

        result = markdown_to_blocks(markdown)

        AssertEqualLists(self, result, expected)
    
    def test_markdown_to_blocks_empty(self):
        markdown = ""
        expected = []
        result = markdown_to_blocks(markdown)
        AssertEqualLists(self, result, expected)

class TestBlockToBlockType(unittest.TestCase):
    def test_block_to_blocktype_heading(self):
        block = "# Heading 1"
        expected = BlockType.HEADING
        result = block_to_blocktype(block)
        self.assertEqual(result, expected)
    
    def test_block_to_blocktype_code(self):
        block = "```Here's some\ncode()\nwith multiple lines\nand symbols[]```"
        expected = BlockType.CODE
        result = block_to_blocktype(block)
        self.assertEqual(result, expected)

    def test_block_to_blocktype_quote(self):
        block = "> This is a quote\n> with multiple lines"
        expected = BlockType.QUOTE
        result = block_to_blocktype(block)
        self.assertEqual(result, expected)
    
    def test_block_to_blocktype_ul(self):
        block = "- This is an unordered list\n- with multiple items"
        expected = BlockType.UNORDERED_LIST
        result = block_to_blocktype(block)
        self.assertEqual(result, expected)
    
    def test_block_to_blocktype_ol(self):
        block = "1. This is an ordered list\n2. with multiple items\n3. and (extra) symbols."
        expected = BlockType.ORDERED_LIST
        result = block_to_blocktype(block)
        self.assertEqual(result, expected)
    
    def test_block_to_blocktype_paragraph(self):
        block = "This is a simple paragraph\nwith no special formatting."
        expected = BlockType.PARAGRAPH
        result = block_to_blocktype(block)
        self.assertEqual(result, expected)
    
    def test_block_to_blocktype_empty(self):
        block = ""
        expected = BlockType.PARAGRAPH
        result = block_to_blocktype(block)
        self.assertEqual(result, expected)
    
    def test_block_to_blocktype_partial(self):
        block = "This is **a block** with\n``some incomplete formatting - extra\nsymbols (like # hashtags)\n- and stuff."
        expected = BlockType.PARAGRAPH
        result = block_to_blocktype(block)
        self.assertEqual(result, expected)

if (__name__ == "__main__"):
    unittest.main()
