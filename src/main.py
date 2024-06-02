from textnode import TextNode
from leafnode import LeafNode
from parentnode import ParentNode


def main():
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
            LeafNode(None, "Normal text"),
        ],
    )
    print(node.to_html())


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case "text":
            return LeafNode(value=text_node.text)
        case "bold":
            return LeafNode("b", text_node.text)
        case "italic":
            return LeafNode("i", text_node.text)
        case "code":
            return LeafNode("code", text_node.text)
        case "link":
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case "image":
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("Unknown text type for TextNode.")


main()
