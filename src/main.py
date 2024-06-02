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


main()
