import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

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

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_i(self):
        node = LeafNode("i", "Nevermore")
        self.assertEqual(node.to_html(), "<i>Nevermore</i>")
    
    def test_leaf_to_html_a(self):
        node = LeafNode("a","This is boots", {"href": "https://www.boot.dev/dashboard"})
        self.assertEqual(node.to_html(), '<a href="https://www.boot.dev/dashboard">This is boots</a>')
    
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    def test_to_html_without_children(self):
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError) as cm:
            parent_node.to_html()
        self.assertIn("Children not found", str(cm.exception))
    def test_to_html_multiple_children(self):
        child_nodes = [LeafNode("b", "child1"), LeafNode("i", "child2")]
        parent_node = ParentNode("div", child_nodes)
        self.assertEqual(
            parent_node.to_html(),
            "<div><b>child1</b><i>child2</i></div>",
        )
if __name__ == "__main__":
    unittest.main()