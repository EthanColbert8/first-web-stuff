import unittest

from src.MDtoHTML import markdown_to_html_node

class TestMDtoHTML(unittest.TestCase):
    def test_MDtoHTML_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        expected = "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>"

        html_node = markdown_to_html_node(md)
        self.assertEqual(html_node.to_html(), expected)
    
    def test_MDtoHTML_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        expected = "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>"

        html_node = markdown_to_html_node(md)
        self.assertEqual(html_node.to_html(), expected)
    
    def test_MDtoHTML_empty(self):
        md = ""
        expected = "<div></div>"

        html_node = markdown_to_html_node(md)
        self.assertEqual(html_node.to_html(), expected)
    
    def test_MDtoHTML_headings(self):
        md = """
# Heading the First

This is some _paragrap_ text inside.

### Heading the Lesser

Some more paragraph text can go here.
"""
        expected = "<div><h1>Heading the First</h1><p>This is some <i>paragrap</i> text inside.</p><h3>Heading the Lesser</h3><p>Some more paragraph text can go here.</p></div>"

        html_node = markdown_to_html_node(md)
        self.assertEqual(html_node.to_html(), expected)
    
    def test_MDtoHDML_lists(self):
        md = """
Here's some paragraph text before a list:

- Unordered item
- Another unordered item
- Another one
- One **with some** _pizzazz_ to it

A bit of text between the lists makes it nice.

1. Here's an
2. Ordered list.
3. We can put **stuff** inside it too.
"""
        expected = "<div><p>Here's some paragraph text before a list:</p><ul><li>Unordered item</li><li>Another unordered item</li><li>Another one</li><li>One <b>with some</b> <i>pizzazz</i> to it</li></ul><p>A bit of text between the lists makes it nice.</p><ol><li>Here's an</li><li>Ordered list.</li><li>We can put <b>stuff</b> inside it too.</li></ol></div>"

        html_node = markdown_to_html_node(md)
        self.assertEqual(html_node.to_html(), expected)

if (__name__ == "__main__"):
    unittest.main()
