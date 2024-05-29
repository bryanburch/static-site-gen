import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_render_p_tag(self):
        node = LeafNode("p", "This is a paragraph of text.")
        node_html = "<p>This is a paragraph of text.</p>"
        self.assertEqual(node.to_html(), node_html)

    def test_render_a_tag(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        node_html = '<a href="https://www.google.com">Click me!</a>'
        self.assertEqual(node.to_html(), node_html)

    def test_render_raw_text(self):
        node = LeafNode(value="Raw text.")
        node_html = "Raw text."
        self.assertEqual(node.to_html(), node_html)


if __name__ == "__main__":
    unittest.main()
