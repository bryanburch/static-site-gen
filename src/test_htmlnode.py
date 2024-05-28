import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        props = {"href": "https://www.google.com", "target": "_blank"}
        node = HTMLNode(tag="a", value="Google", props=props)

        props_html = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), props_html)

    def test_props_to_html_none(self):
        node = HTMLNode(tag="p", value="Google")
        props_html = ""
        self.assertEqual(node.props_to_html(), props_html)
    
    def test_repr(self):
        props = {"href": "https://www.google.com", "target": "_blank"}
        node = HTMLNode(tag="a", value="Google", props=props)

        node_repr = f"HTMLNode(a, Google, None, {props})"
        self.assertEqual(repr(node), node_repr)


if __name__ == "__main__":
    unittest.main()