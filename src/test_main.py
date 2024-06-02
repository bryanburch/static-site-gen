import unittest

from textnode import TextNode
from leafnode import LeafNode
from main import text_node_to_html_node


class TestMain(unittest.TestCase):
    def test_text_node_to_html_node_text_type(self):
        text_node = TextNode("Test", "text")
        html_node = text_node_to_html_node(text_node)

        self.assertEqual(html_node, LeafNode(None, "Test"))

    def test_text_node_to_html_node_bold_type(self):
        text_node = TextNode("Test", "bold")
        html_node = text_node_to_html_node(text_node)

        self.assertEqual(html_node, LeafNode("b", "Test"))

    def test_text_node_to_html_node_italic_type(self):
        text_node = TextNode("Test", "italic")
        html_node = text_node_to_html_node(text_node)

        self.assertEqual(html_node, LeafNode("i", "Test"))

    def test_text_node_to_html_node_code_type(self):
        text_node = TextNode("Test", "code")
        html_node = text_node_to_html_node(text_node)

        self.assertEqual(html_node, LeafNode("code", "Test"))

    def test_text_node_to_html_node_link_type(self):
        text_node = TextNode("Test", "link", "https://www.google.com")
        html_node = text_node_to_html_node(text_node)

        self.assertEqual(
            html_node, LeafNode("a", "Test", {"href": "https://www.google.com"})
        )

    def test_text_node_to_html_node_image_type(self):
        text_node = TextNode("Test", "image", "https://www.google.com/img.jpg")
        html_node = text_node_to_html_node(text_node)

        self.assertEqual(
            html_node,
            LeafNode(
                "img", "", {"src": "https://www.google.com/img.jpg", "alt": "Test"}
            ),
        )

    def test_text_node_to_html_node_unknown_type(self):
        error = None
        try:
            text_node = TextNode("Test", "underline")
            html_node = text_node_to_html_node(text_node)
        except Exception as e:
            error = str(e)
        self.assertEqual(error, "Unknown text type for TextNode.")


if __name__ == "__main__":
    unittest.main()
