import unittest

from parentnode import ParentNode
from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_parent_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        node_html = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(node.to_html(), node_html)

    def test_parent_to_html_nesting_one_branch(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                ParentNode(
                    "ol",
                    [
                        LeafNode("li", "Item 1"),
                        LeafNode("li", "Item 2"),
                        LeafNode("li", "Item 3"),
                    ],
                ),
            ],
        )
        node_html = "<p><b>Bold text</b><ol><li>Item 1</li><li>Item 2</li><li>Item 3</li></ol></p>"
        self.assertEqual(node.to_html(), node_html)

    def test_parent_to_html_nesting_multiple_branches(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                ParentNode(
                    "ol",
                    [
                        LeafNode("li", "Item 1"),
                        LeafNode("li", "Item 2"),
                        LeafNode("li", "Item 3"),
                    ],
                ),
                LeafNode("i", "italic text"),
                ParentNode(
                    "ol",
                    [
                        LeafNode("li", "Item 1"),
                        LeafNode("li", "Item 2"),
                        LeafNode("li", "Item 3"),
                    ],
                ),
            ],
        )
        node_html = (
            "<p><b>Bold text</b><ol><li>Item 1</li><li>Item 2</li><li>Item 3</li></ol>"
            "<i>italic text</i><ol><li>Item 1</li><li>Item 2</li><li>Item 3</li></ol></p>"
        )
        self.assertEqual(node.to_html(), node_html)

    def test_parent_to_html_deep_nesting(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                ParentNode(
                    "ol",
                    [
                        LeafNode("li", "Item 1"),
                        ParentNode(
                            "ul",
                            [
                                LeafNode("li", "Bullet"),
                                LeafNode("li", "Bullet"),
                            ],
                        ),
                        LeafNode("li", "Item 2"),
                    ],
                ),
            ],
        )
        node_html = (
            "<p><b>Bold text</b><ol><li>Item 1</li><ul><li>Bullet</li>"
            "<li>Bullet</li></ul><li>Item 2</li></ol></p>"
        )
        self.assertEqual(node.to_html(), node_html)

    def test_parent_to_html_no_tag(self):
        error = None
        try:
            node = ParentNode(None, LeafNode("b", "Bold text"))
            node.to_html()
        except ValueError as e:
            error = str(e)
        self.assertEqual(error, "ParentNode tag attribute cannot be None.")

    def test_parent_to_html_no_children(self):
        error = None
        try:
            node = ParentNode("ol", None)
            node.to_html()
        except ValueError as e:
            error = str(e)
        self.assertEqual(error, "ParentNode children attribute cannot be None.")


if __name__ == "__main__":
    unittest.main()
