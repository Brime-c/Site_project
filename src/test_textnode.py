import unittest

from textnode import TextNode, TextType, text_node_to_html_node


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
        node = TextNode("this is a text node", TextType.LINK, url=None)
        node2 = TextNode("this is a text node", TextType.LINK, url=None)
        self.assertEqual(node,node2)
    def test_different_url(self):
        node = TextNode("this is a text node", TextType.LINK, url="A")
        node2 = TextNode("this is a text node", TextType.LINK, url="B")
        self.assertNotEqual(node,node2)
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    def test_bold(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")
    def test_italic(self):
        node = TextNode("This is an italic text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic text node")
    def test_code(self):
        node = TextNode("This is a code text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code text node")
    def test_link(self):
        node = TextNode("This is a link text node", TextType.LINK, "www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.props, {"href": "www.boot.dev"})
        self.assertEqual(html_node.value, "This is a link text node")
    def test_image(self):
        node = TextNode("This is an image text node", TextType.IMAGE, "www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.props, {"src": "www.boot.dev", "alt": "This is an image text node"})
        
if __name__ == "__main__":
    unittest.main()