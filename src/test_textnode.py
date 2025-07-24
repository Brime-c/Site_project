import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    def test_neq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)
    def test_different_text(self):
        node = TextNode("this is a text node", TextType.BOLD)
        node2 = TextNode("this is a banana", TextType.BOLD)
        self.assertNotEqual(node,node2)
    def test_url(self):
        node = TextNode("this is a text node", TextType.LINKS, url=None)
        node2 = TextNode("this is a text node", TextType.LINKS, url=None)
        self.assertEqual(node,node2)
    def test_different_url(self):
        node = TextNode("this is a text node", TextType.LINKS, url="A")
        node2 = TextNode("this is a text node", TextType.LINKS, url="B")
        self.assertNotEqual(node,node2)
if __name__ == "__main__":
    unittest.main()