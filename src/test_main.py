import unittest

from parentnode import ParentNode
from textnode import TextNode
from leafnode import LeafNode
from main import (
    block_to_block_type,
    markdown_to_blocks,
    split_nodes_link,
    text_node_to_html_node,
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    text_to_textnodes,
    markdown_to_html_node,
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

    def test_is_paragraph(self):
        text = "This is a paragraph."

        self.assertEqual(block_to_block_type(text), "paragraph")

    def test_is_heading(self):
        text = "## This is a heading."

        self.assertEqual(block_to_block_type(text), "heading")

    def test_is_heading_invalid(self):
        text = "-# This is a heading."

        self.assertEqual(block_to_block_type(text), "paragraph")

    def test_is_code(self):
        text = "```This is a code block```"

        self.assertEqual(block_to_block_type(text), "code")

    def test_is_code_invalid(self):
        text = "``This is an invalid code block```"

        self.assertEqual(block_to_block_type(text), "paragraph")

    def test_is_quote(self):
        text = "> This is a quote"

        self.assertEqual(block_to_block_type(text), "quote")

    def test_is_quote_invalid(self):
        text = ">This is an invalid quote"

        self.assertEqual(block_to_block_type(text), "paragraph")

    def test_is_unordered_list(self):
        text = """
* This is a list item
* Another item
- Yet another item
* Some other text
- And one more item
"""

        self.assertEqual(block_to_block_type(text), "unordered_list")

    def test_is_unordered_list_invalid(self):
        text = """
* This is a list item
* Another item
-Yet another item
* Some other text
- And one more item
"""

        self.assertEqual(block_to_block_type(text), "paragraph")

    def test_is_ordered_list(self):
        text = """
1. This is a list item
2. Another item
3. Yet another item
4. Some other text
5. And one more item
"""

        self.assertEqual(block_to_block_type(text), "ordered_list")

    def test_is_ordered_list_invalid(self):
        text = """
1. This is a list item
2 Another item
3. Yet another item
4. Some other text
5. And one more item
"""

        self.assertEqual(block_to_block_type(text), "paragraph")

    def test_markdown_to_html_node_just_heading(self):
        markdown = "# H1 heading."
        html_node = markdown_to_html_node(markdown)

        expected = ParentNode(
            tag="div",
            children=ParentNode(
                tag=f"h1", children=LeafNode(tag=None, value="H1 heading.")
            ),
        )
        self.assertEqual(html_node, expected)

    def test_markdown_to_html_node_heading_with_inline(self):
        markdown = "# A *fancy* heading."
        html_node = markdown_to_html_node(markdown)

        expected = ParentNode(
            tag="div",
            children=ParentNode(
                tag=f"h1",
                children=[
                    LeafNode(tag=None, value="A "),
                    LeafNode(tag="i", value="fancy"),
                    LeafNode(tag=None, value=" heading."),
                ],
            ),
        )
        self.assertEqual(html_node, expected)

    def test_markdown_to_html_node_just_code(self):
        markdown = "```import pandas as pd```"
        html_node = markdown_to_html_node(markdown)

        expected = ParentNode(
            tag="div",
            children=ParentNode(
                tag="pre",
                children=ParentNode(
                    tag=f"code",
                    children=LeafNode(tag=None, value="import pandas as pd"),
                ),
            ),
        )
        self.assertEqual(html_node, expected)

    def test_markdown_to_html_node_code_with_inline(self):
        markdown = "```import **pandas** as **pd**```"
        html_node = markdown_to_html_node(markdown)

        expected = ParentNode(
            tag="div",
            children=ParentNode(
                tag="pre",
                children=ParentNode(
                    tag=f"code",
                    children=[
                        LeafNode(tag=None, value="import "),
                        LeafNode(tag="b", value="pandas"),
                        LeafNode(tag=None, value=" as "),
                        LeafNode(tag="b", value="pd"),
                    ],
                ),
            ),
        )
        self.assertEqual(html_node, expected)

    def test_markdown_to_html_node_just_quote(self):
        markdown = "> Part of the journey is the end."
        html_node = markdown_to_html_node(markdown)

        expected = ParentNode(
            tag="div",
            children=ParentNode(
                tag="blockquote",
                children=LeafNode(tag=None, value="Part of the journey is the end."),
            ),
        )
        self.assertEqual(html_node, expected)

    def test_markdown_to_html_node_quote_with_inline(self):
        markdown = "> Part of the journey is the end. - [Stark](https://www.youtube.com/watch?v=TcMBFSGVi1c)"
        html_node = markdown_to_html_node(markdown)

        expected = ParentNode(
            tag="div",
            children=ParentNode(
                tag="blockquote",
                children=[
                    LeafNode(tag=None, value="Part of the journey is the end. - "),
                    LeafNode(
                        tag="a",
                        value="Stark",
                        props={"href": "https://www.youtube.com/watch?v=TcMBFSGVi1c"},
                    ),
                ],
            ),
        )
        self.assertEqual(html_node, expected)

    def test_markdown_to_html_node_just_unordered_list(self):
        markdown = """- Apples
- Bananas
- Oranges"""
        html_node = markdown_to_html_node(markdown)

        expected = ParentNode(
            tag="div",
            children=ParentNode(
                tag="ul",
                children=[
                    ParentNode(tag="li", children=LeafNode(value="Apples")),
                    ParentNode(tag="li", children=LeafNode(value="Bananas")),
                    ParentNode(tag="li", children=LeafNode(value="Oranges")),
                ],
            ),
        )
        self.assertEqual(html_node, expected)

    def test_markdown_to_html_node_unordered_list_with_inline(self):
        markdown = """- Apples ![Apple Inc.](https://upload.wikimedia.org/wikipedia/commons/thumb/f/fa/Apple_logo_black.svg/135px-Apple_logo_black.svg.png)
- Bananas
- Oranges"""
        html_node = markdown_to_html_node(markdown)

        expected = ParentNode(
            tag="div",
            children=ParentNode(
                tag="ul",
                children=[
                    ParentNode(
                        tag="li",
                        children=[
                            LeafNode(value="Apples "),
                            LeafNode(
                                tag="img",
                                value="",
                                props={
                                    "src": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fa/Apple_logo_black.svg/135px-Apple_logo_black.svg.png",
                                    "alt": "Apple Inc.",
                                },
                            ),
                        ],
                    ),
                    ParentNode(tag="li", children=LeafNode(value="Bananas")),
                    ParentNode(tag="li", children=LeafNode(value="Oranges")),
                ],
            ),
        )
        self.assertEqual(html_node, expected)

    def test_markdown_to_html_node_just_ordered_list(self):
        markdown = """1. Morning
2. Afternoon
3. Evening"""
        html_node = markdown_to_html_node(markdown)

        expected = ParentNode(
            tag="div",
            children=ParentNode(
                tag="ol",
                children=[
                    ParentNode(tag="li", children=LeafNode(value="Morning")),
                    ParentNode(tag="li", children=LeafNode(value="Afternoon")),
                    ParentNode(tag="li", children=LeafNode(value="Evening")),
                ],
            ),
        )
        self.assertEqual(html_node, expected)

    def test_markdown_to_html_node_ordered_list_with_inline(self):
        markdown = """1. First there's morning
2. *Then* there's afternoon
3. **Finally** there's evening"""
        html_node = markdown_to_html_node(markdown)

        expected = ParentNode(
            tag="div",
            children=ParentNode(
                tag="ol",
                children=[
                    ParentNode(
                        tag="li", children=LeafNode(value="First there's morning")
                    ),
                    ParentNode(
                        tag="li",
                        children=[
                            LeafNode(tag="i", value="Then"),
                            LeafNode(value=" there's afternoon"),
                        ],
                    ),
                    ParentNode(
                        tag="li",
                        children=[
                            LeafNode(tag="b", value="Finally"),
                            LeafNode(value=" there's evening"),
                        ],
                    ),
                ],
            ),
        )
        self.assertEqual(html_node, expected)

    def test_markdown_to_html_node_just_paragraph(self):
        markdown = "This is a paragraph of text."
        html_node = markdown_to_html_node(markdown)

        expected = ParentNode(
            tag="div",
            children=ParentNode(
                tag="p", children=LeafNode(value="This is a paragraph of text.")
            ),
        )
        self.assertEqual(html_node, expected)

    def test_markdown_to_html_node_paragraph_with_inline(self):
        markdown = "This is a paragraph of text. It has some **bold** and *italic* words inside of it."
        html_node = markdown_to_html_node(markdown)

        expected = ParentNode(
            tag="div",
            children=ParentNode(
                tag="p",
                children=[
                    LeafNode(value="This is a paragraph of text. It has some "),
                    LeafNode(tag="b", value="bold"),
                    LeafNode(value=" and "),
                    LeafNode(tag="i", value="italic"),
                    LeafNode(value=" words inside of it."),
                ],
            ),
        )
        self.assertEqual(html_node, expected)

    def test_markdown_to_html_node_multiple_blocks(self):
        markdown = """# This is a heading

This is a paragraph of text.

* This is the first list item in a list block
* This is a list item
* This is another list item
"""
        html_node = markdown_to_html_node(markdown)

        expected = ParentNode(
            tag="div",
            children=[
                ParentNode(tag="h1", children=LeafNode(value="This is a heading")),
                ParentNode(
                    tag="p", children=LeafNode(value="This is a paragraph of text.")
                ),
                ParentNode(
                    tag="ul",
                    children=[
                        ParentNode(
                            tag="li",
                            children=LeafNode(
                                value="This is the first list item in a list block"
                            ),
                        ),
                        ParentNode(
                            tag="li", children=LeafNode(value="This is a list item")
                        ),
                        ParentNode(
                            tag="li",
                            children=LeafNode(value="This is another list item"),
                        ),
                    ],
                ),
            ],
        )

        self.assertEqual(html_node, expected)

    def test_markdown_to_html_node_multiple_blocks_with_inline(self):
        markdown = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item
"""
        html_node = markdown_to_html_node(markdown)

        expected = ParentNode(
            tag="div",
            children=[
                ParentNode(tag="h1", children=LeafNode(value="This is a heading")),
                ParentNode(
                    tag="p",
                    children=[
                        LeafNode(value="This is a paragraph of text. It has some "),
                        LeafNode(tag="b", value="bold"),
                        LeafNode(value=" and "),
                        LeafNode(tag="i", value="italic"),
                        LeafNode(value=" words inside of it."),
                    ],
                ),
                ParentNode(
                    tag="ul",
                    children=[
                        ParentNode(
                            tag="li",
                            children=LeafNode(
                                value="This is the first list item in a list block"
                            ),
                        ),
                        ParentNode(
                            tag="li", children=LeafNode(value="This is a list item")
                        ),
                        ParentNode(
                            tag="li",
                            children=LeafNode(value="This is another list item"),
                        ),
                    ],
                ),
            ],
        )

        self.assertEqual(html_node, expected)


if __name__ == "__main__":
    unittest.main()
