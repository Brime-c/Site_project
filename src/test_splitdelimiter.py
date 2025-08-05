import unittest

from textnode import TextNode, TextType
from splitdelimiter import split_nodes_delimiter

class TestSplitDelimiter(unittest.TestCase):
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
    def no_delimiter(self):
        node = TextNode("hello, how are you", TextType.TEXT)
        result = split_nodes_delimiter([node],"**", TextType.BOLD)
        expected = [TextNode("hello, how are you", TextType.TEXT)]
        self.assertEqual(result,expected)
    def lead_delimiter(self):
        node = TextNode("**bold** text node", TextType.TEXT)
        result = split_nodes_delimiter([node],"**", TextType.BOLD)
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode(" text node", TextType.TEXT)
        ]
        self.assertEqual(result, expected)
    def unmatched_delimiter(self):
        node = TextNode("this is not a **bold text node", TextType.TEXT)
        with self.assertRaises(Exception) as cm:
            split_nodes_delimiter([node],"**", TextType.BOLD)
        self.assertIn("unmatched delimiter found", str(cm.exception))
if __name__ == "__main__":
    unittest.main()