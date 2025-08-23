import unittest

from textnode import TextNode, TextType
from main import extract_title


class TestMain(unittest.TestCase):
    def test_title(self):
        md = "# hello how are you"
        header = extract_title(md)
        self.assertEqual(header, "hello how are you")
    def test_no_title(self):
        md = "hello how are you"
        with self.assertRaises(Exception) as cm:    
            header = extract_title(md)
        self.assertIn("no title found", str(cm.exception))
    def test_mid_title(self):
        md = """
hello how are you
# this is a title 
"""
        header = extract_title(md)
        self.assertEqual(header, "this is a title")
    def test_multi_title(self):
        md = " ## hello this is not a title"
        with self.assertRaises(Exception) as cm:
            header = extract_title(md)
        self.assertIn("no title found", str(cm.exception))
    def test_extra_space(self):
        md = " # this should be a title "
        header = extract_title(md)
        self.assertEqual(header, "this should be a title")