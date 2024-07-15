import unittest

from textnode import TextNode
from leafnode import LeafNode
from main import (
    markdown_to_blocks,
    split_nodes_link,
    text_node_to_html_node,
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    text_to_textnodes,
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

    def test_split_nodes_image(self):
        node = TextNode(
            "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
            "text",
        )
        new_nodes = split_nodes_image([node])

        expected = [
            TextNode("This is text with an ", "text"),
            TextNode(
                "image",
                "image",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            TextNode(" and another ", "text"),
            TextNode(
                "second image",
                "image",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png",
            ),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_image_no_image(self):
        node = TextNode(
            "This is text without an image.",
            "text",
        )
        new_nodes = split_nodes_image([node])

        expected = [
            TextNode("This is text without an image.", "text"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_image_at_start(self):
        node = TextNode(
            "![Image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
            "text",
        )
        new_nodes = split_nodes_image([node])

        expected = [
            TextNode(
                "Image",
                "image",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            TextNode(" and another ", "text"),
            TextNode(
                "second image",
                "image",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png",
            ),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_link(self):
        node = TextNode(
            "This is text with an [link](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another [link](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
            "text",
        )
        new_nodes = split_nodes_link([node])

        expected = [
            TextNode("This is text with an ", "text"),
            TextNode(
                "link",
                "link",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            TextNode(" and another ", "text"),
            TextNode(
                "link",
                "link",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png",
            ),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_link_no_link(self):
        node = TextNode(
            "This is text without a link.",
            "text",
        )
        new_nodes = split_nodes_link([node])

        expected = [
            TextNode("This is text without a link.", "text"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_link_at_start(self):
        node = TextNode(
            "[Link](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another [link](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
            "text",
        )
        new_nodes = split_nodes_link([node])

        expected = [
            TextNode(
                "Link",
                "link",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
            ),
            TextNode(" and another ", "text"),
            TextNode(
                "link",
                "link",
                "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png",
            ),
        ]
        self.assertEqual(new_nodes, expected)

    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", "text"),
            TextNode("text", "bold"),
            TextNode(" with an ", "text"),
            TextNode("italic", "italic"),
            TextNode(" word and a ", "text"),
            TextNode("code block", "code"),
            TextNode(" and an ", "text"),
            TextNode("obi wan image", "image", "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", "text"),
            TextNode("link", "link", "https://boot.dev"),
        ]
        self.assertEqual(nodes, expected)

    def test_text_to_textnodes_just_text(self):
        text = "This is text."
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is text.", "text"),
        ]
        self.assertEqual(nodes, expected)

    def test_text_to_textnodes_just_bold(self):
        text = "**This is bold.**"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is bold.", "bold"),
        ]
        self.assertEqual(nodes, expected)

    def test_text_to_textnodes_just_italic(self):
        text = "*This is italic.*"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is italic.", "italic"),
        ]
        self.assertEqual(nodes, expected)

    def test_text_to_textnodes_just_italic(self):
        text = "`This is code.`"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is code.", "code"),
        ]
        self.assertEqual(nodes, expected)

    def test_text_to_textnodes_just_image(self):
        text = "![Image](https://i.imgur.com/fJRm4Vk.jpeg)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("Image", "image", "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        self.assertEqual(nodes, expected)

    def test_text_to_textnodes_just_link(self):
        text = "[Link](https://i.imgur.com/fJRm4Vk.jpeg)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("Link", "link", "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        self.assertEqual(nodes, expected)

    def test_text_to_textnodes_empty_string(self):
        text = ""
        nodes = text_to_textnodes(text)
        expected = []
        self.assertEqual(nodes, expected)

    def test_text_to_textnodes_many_same_delimiter(self):
        text = "**This** is **text** with **alternating** bold **words**."
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This", "bold"),
            TextNode(" is ", "text"),
            TextNode("text", "bold"),
            TextNode(" with ", "text"),
            TextNode("alternating", "bold"),
            TextNode(" bold ", "text"),
            TextNode("words", "bold"),
            TextNode(".", "text"),
        ]
        self.assertEqual(nodes, expected)

    def test_markdown_to_blocks(self):
        markdown = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"""

        blocks = markdown_to_blocks(markdown)

        expected = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            """* This is the first list item in a list block
* This is a list item
* This is another list item""",
        ]

        self.assertEqual(blocks, expected)

    def test_markdown_to_blocks_single(self):
        markdown = "  # This is a heading "

        blocks = markdown_to_blocks(markdown)

        expected = ["# This is a heading"]

        self.assertEqual(blocks, expected)

    def test_markdown_to_blocks_trailing_new_lines(self):
        markdown = """  # This is a heading

        
          
        """

        blocks = markdown_to_blocks(markdown)

        expected = ["# This is a heading"]

        self.assertEqual(blocks, expected)

    def test_markdown_to_blocks_empty_string(self):
        markdown = """ 

        
          
        """

        blocks = markdown_to_blocks(markdown)

        expected = []

        self.assertEqual(blocks, expected)


if __name__ == "__main__":
    unittest.main()
