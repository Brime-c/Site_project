import unittest

from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes
class TestInlineMarkdown(unittest.TestCase):
    def test_one_delimiter(self):
        node = TextNode("this is a **bold** text", TextType.TEXT)
        result = split_nodes_delimiter([node],"**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("this is a ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ],
            result
        )

    def test_mult_delimiter(self):
        node = TextNode("hello **you** are seeing a **bold** text node",TextType.TEXT)
        result = split_nodes_delimiter([node],"**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("hello ", TextType.TEXT),
                TextNode("you", TextType.BOLD),
                TextNode(" are seeing a ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text node", TextType.TEXT)
            ],
            result
        )
        

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

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "this is a text with a [link](https://www.boot.dev) and another [second link](https://www.boot.dev/dashboard)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("this is a text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://www.boot.dev/dashboard"
                    ),
            ],
            new_nodes
        )

    def test_split_none(self):
        node = TextNode(
            "this is a text node with no links or images", TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("this is a text node with no links or images", TextType.TEXT)
            ],
            new_nodes
        )

    def test_split_empty(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([], new_nodes
        )

    def test_split_only_links(self):
        node = TextNode("[link](https://www.boot.dev)[second link](https://www.boot.dev/dashboard)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
                TextNode("second link", TextType.LINK, "https://www.boot.dev/dashboard")
            ],
            new_nodes
        )
    
    def test_text_to_textnodes(self):
        node = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
            
        new_nodes = text_to_textnodes(node)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes
        )
if __name__ == "__main__":
    unittest.main()