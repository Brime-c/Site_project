import unittest

from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links

class TestInlineMarkdown(unittest.TestCase):
    def test_one_delimiter(self):
        node = TextNode("this is a **bold** text", TextType.TEXT)
        result = split_nodes_delimiter([node],"**", TextType.BOLD)
        expected = [
            TextNode("this is a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_mult_delimiter(self):
        node = TextNode("hello **you** are seeing a **bold** text node",TextType.TEXT)
        result = split_nodes_delimiter([node],"**", TextType.BOLD)
        expected = [
            TextNode("hello ", TextType.TEXT),
            TextNode("you", TextType.BOLD),
            TextNode(" are seeing a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text node", TextType.TEXT)
        ]
        self.assertEqual(result,expected)

    def test_no_delimiter(self):
        node = TextNode("hello, how are you", TextType.TEXT)
        result = split_nodes_delimiter([node],"**", TextType.BOLD)
        expected = [TextNode("hello, how are you", TextType.TEXT)]
        self.assertEqual(result,expected)

    def test_lead_delimiter(self):
        node = TextNode("**bold** text node", TextType.TEXT)
        result = split_nodes_delimiter([node],"**", TextType.BOLD)
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode(" text node", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_unmatched_delimiter(self):
        node = TextNode("this is not a **bold text node", TextType.TEXT)
        with self.assertRaises(Exception) as cm:
            split_nodes_delimiter([node],"**", TextType.BOLD)
        self.assertIn("unmatched delimiter found", str(cm.exception))

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
            )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

if __name__ == "__main__":
    unittest.main()