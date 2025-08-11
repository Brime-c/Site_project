import unittest

from textnode import TextNode, TextType
from block_markdown import markdown_to_blocks

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
if __name__ == "__main__":
    unittest.main()