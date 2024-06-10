from textnode import TextNode
from leafnode import LeafNode
from parentnode import ParentNode
from collections import deque


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
    # print(node.to_html())


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


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != "text":
            new_nodes.append(old_node)
            continue

        split_nodes = []
        sections = old_node.text.split(delimiter)

        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")

        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], "text"))
            else:
                split_nodes.append(TextNode(sections[i], text_type))

        new_nodes.extend(split_nodes)
    return new_nodes


# def split_nodes_delimiter(old_nodes, delimiter, text_type):
#     new_nodes = []
#     delimiter_stack = deque()
#     for old_node in old_nodes:
#         if not isinstance(old_node, TextNode):
#             new_nodes.append(old_node)
#             continue

#         text = ""
#         for c in old_node.text:
#             if c == delimiter:
#                 if delimiter_stack:
#                     new_nodes.append(TextNode(text, text_type))
#                     delimiter_stack.pop()
#                     text = ""
#                 else:
#                     new_nodes.append(TextNode(text, "text"))
#                     delimiter_stack.append(c)
#                     text = ""
#             else:
#                 text += c
#         if text:
#             new_nodes.append(TextNode(text, "text"))

#         if delimiter_stack:
#             raise Exception(
#                 f"Invalid Markdown syntax for text '{old_node.text}', using delimiter '{delimiter}'."
#             )

#     return new_nodes


# old implementation with multiple nodes issue (italic, bold)
# def split_nodes_delimiter(old_nodes, delimiter, text_type):
#     text_type_text = "text"

#     new_nodes = []
#     for node in old_nodes:
#         if not isinstance(node, TextNode):
#             new_nodes.append(node)
#             continue

#         num_delimiters = node.text.count(delimiter)
#         if num_delimiters % 2 > 0:
#             raise Exception(
#                 f"Invalid Markdown syntax for text '{node.text}', using delimiter '{delimiter}'."
#             )

#         strings = node.text.split(delimiter)
#         prev_text_type = None
#         for s in range(len(strings)):
#             if s == 0 and not strings[s]:
#                 prev_text_type = text_type_text
#                 continue
#             if s == len(strings) - 3 and not strings[s]:
#                 prev_text_type = text_type_text
#                 continue
#             if s == len(strings) - 1 and not strings[s]:
#                 break

#             if prev_text_type != text_type_text:
#                 new_nodes.append(TextNode(strings[s], text_type_text))
#                 prev_text_type = text_type_text
#             else:
#                 new_nodes.append(TextNode(strings[s], text_type))
#                 prev_text_type = text_type

#     return new_nodes


main()
