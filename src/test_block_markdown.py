import unittest

from textnode import TextNode, TextType
from block_markdown import markdown_to_blocks, block_to_block, BlockType, markdown_to_html_node

class TestInblockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    def test_markdown_to_blocks_with_extra_newlines(self):
        md = """


First block


Second block



Third block


"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks,
                         [
                             "First block",
                             "Second block",
                             "Third block",
                         ]
                         )
    def test_markdown_to_blocks_only_newlines(self):
        md = """








"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks,
                         [])
    
    def test_mark_down_to_blocks_one_line(self):
        md = "this is a single line of text"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks,
                         ["this is a single line of text"])
    
    def test_block_to_block_heading(self):
        md = "# this is a heading"
        blocks = block_to_block(md)
        self.assertEqual(blocks, BlockType.HEADING)
    def test_block_to_block_not_heading(self):
        md = "####### this is not a heading"
        blocks = block_to_block(md)
        self.assertEqual(blocks, BlockType.PARAGRAPH)

    def test_block_to_block_code(self):
        md = "```\nthis is code\n```"
        blocks = block_to_block(md)
        self.assertEqual(blocks, BlockType.CODE)
    def test_block_to_block_not_code(self):
        md = "``` this is not code ```"
        blocks = block_to_block(md)
        self.assertEqual(blocks, BlockType.PARAGRAPH)
    
    def test_block_to_block_quote(self):
        md = ">this is\n>a quote"
        blocks = block_to_block(md)
        self.assertEqual(blocks, BlockType.QUOTE)
    def test_block_to_block_not_quote(self):
        md = "> this is \nnot a quote"
        blocks = block_to_block(md)
        self.assertEqual(blocks, BlockType.PARAGRAPH)
    
    def test_block_to_block_UL(self):
        md = "- this is\n- an unordered list"
        blocks = block_to_block(md)
        self.assertEqual(blocks, BlockType.UNORDERED_LIST)
    def test_block_to_block_not_UL(self):
        md = "-this is not\n- and unordered list"
        blocks = block_to_block(md)
        self.assertEqual(blocks, BlockType.PARAGRAPH)
    
    def test_block_to_block_OL(self):
        md = "1. this\n2. is an\n3. ordered list"
        blocks = block_to_block(md)
        self.assertEqual(blocks, BlockType.ORDERED_LIST)
    def test_block_to_block_not_OL(self):
        md = "1. this\n1. is not\n3. an ordered list"
        blocks = block_to_block(md)
        self.assertEqual(blocks, BlockType.PARAGRAPH)

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
    
    def test_quote(self):
        md = """
>this is a **bold** 
>quote text with _italic_ words
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>this is a <b>bold</b> quote text with <i>italic</i> words</blockquote></div>"
        )
    def test_heading(self):
        md = "#### this is a heading with a **bold** text"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h4>this is a heading with a <b>bold</b> text</h4></div>"
        )
    def test_unordered_list(self):
        md = """
- this is the first **bold** item
- this is the second _italic_ item
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>this is the first <b>bold</b> item</li><li>this is the second <i>italic</i> item</li></ul></div>"
        )
    def test_ordered_list(self):
        md = """
1. this is the first **bold** item
2. this is the second _italic_ item
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>this is the first <b>bold</b> item</li><li>this is the second <i>italic</i> item</li></ol></div>"
        )
if __name__ == "__main__":
    unittest.main()