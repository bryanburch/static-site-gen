import unittest

from textnode import TextNode
from leafnode import LeafNode
from main import (
    text_node_to_html_node,
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
)


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

    def test_split_nodes_delimiter_code(self):
        node = TextNode("This is text with a `code block` word", "text")
        new_nodes = split_nodes_delimiter([node], "`", "code")

        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", "text"),
                TextNode("code block", "code"),
                TextNode(" word", "text"),
            ],
        )

    def test_split_nodes_delimiter_bold(self):
        node = TextNode("This is text with a **bold** word", "text")
        new_nodes = split_nodes_delimiter([node], "**", "bold")

        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", "text"),
                TextNode("bold", "bold"),
                TextNode(" word", "text"),
            ],
        )

    def test_split_nodes_delimiter_italic(self):
        node = TextNode("This is text with a *italic* word", "text")
        new_nodes = split_nodes_delimiter([node], "*", "italic")

        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", "text"),
                TextNode("italic", "italic"),
                TextNode(" word", "text"),
            ],
        )

    def test_split_nodes_delimiter_start_with(self):
        node = TextNode("*Italic* is what this sentence starts with", "text")
        new_nodes = split_nodes_delimiter([node], "*", "italic")

        self.assertEqual(
            new_nodes,
            [
                TextNode("Italic", "italic"),
                TextNode(" is what this sentence starts with", "text"),
            ],
        )

    def test_split_nodes_delimiter_ends_with(self):
        node = TextNode("This sentence ends with *italic*", "text")
        new_nodes = split_nodes_delimiter([node], "*", "italic")

        self.assertEqual(
            new_nodes,
            [
                TextNode("This sentence ends with ", "text"),
                TextNode("italic", "italic"),
            ],
        )

    def test_extract_markdown_images(self):
        text = (
            "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) "
            "and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        )
        actual = extract_markdown_images(text)

        expected = [
            (
                "image",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            (
                "another",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png",
            ),
        ]

        self.assertEqual(actual, expected)

    def test_extract_markdown_links(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        actual = extract_markdown_links(text)

        expected = [
            ("link", "https://www.example.com"),
            ("another", "https://www.example.com/another"),
        ]

        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
