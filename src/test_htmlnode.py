import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode(tag="a", value="b", children=None, props=None)
        node2 = HTMLNode(tag="a", value="b", children=None, props=None)
        self.assertEqual(node, node2)
    def test_neq(self):
        node = HTMLNode(tag="a", value="b", children=None, props=None)
        node2 = HTMLNode(tag="a", value="c", children=None, props=None)
        self.assertNotEqual(node, node2)
    def test_props_to_html(self):
        node = HTMLNode(tag="tag1", value="value2", children=None, props={"href":"https://www.google.com","target":"_blank"})
        self.assertEqual(' href="https://www.google.com" target="_blank"', node.props_to_html())