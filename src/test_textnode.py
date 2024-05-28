import unittest

from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "italic")
        self.assertNotEqual(node, node2)
    
    def test_url(self):
        node = TextNode("This is a text node", "bold", "https://www.google.com")
        self.assertIsNotNone(node.url)
    
    def test_url_none(self):
        node = TextNode("This is a text node", "bold")
        self.assertIsNone(node.url)

    def test_repr(self):
        node = TextNode("This is a text node", "bold")
        text = "TextNode(This is a text node, bold, None)"
        self.assertEqual(repr(node), text)


if __name__ == "__main__":
    unittest.main()
