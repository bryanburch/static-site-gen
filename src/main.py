import re
from parentnode import ParentNode
from textnode import TextNode
from leafnode import LeafNode


def main():
    # node = TextNode(
    #     "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
    #     "text",
    # )
    # new_nodes = split_nodes_image([node])
    # print(new_nodes)

    markdown = "```import pandas as pd```"
    html_node = markdown_to_html_node(markdown)

    expected = ParentNode(
        tag="div",
        children=ParentNode(
            tag="pre", children=LeafNode(tag=f"code", value="import pandas as pd")
        ),
    )
    print(html_node == expected)


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


def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != "text":
            new_nodes.append(old_node)
            continue

        split_nodes = []
        images = extract_markdown_images(old_node.text)

        if len(images) == 0:
            new_nodes.append(old_node)
            new_nodes.extend(split_nodes)
            continue

        text = old_node.text
        for i in range(len(images)):
            split = text.split(f"![{images[i][0]}]({images[i][1]})", 1)

            # don't create nodes for empty string
            if len(split[0]):
                split_nodes.append(TextNode(split[0], "text"))
            split_nodes.append(TextNode(images[i][0], "image", url=images[i][1]))
            text = split[1]

        if text:
            split_nodes.append(TextNode(text, "text"))

        new_nodes.extend(split_nodes)
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != "text":
            new_nodes.append(old_node)
            continue

        split_nodes = []
        links = extract_markdown_links(old_node.text)

        if len(links) == 0:
            new_nodes.append(old_node)
            new_nodes.extend(split_nodes)
            continue

        text = old_node.text
        for i in range(len(links)):
            split = text.split(f"[{links[i][0]}]({links[i][1]})", 1)

            # don't create nodes for empty string
            if len(split[0]):
                split_nodes.append(TextNode(split[0], "text"))
            split_nodes.append(TextNode(links[i][0], "link", url=links[i][1]))
            text = split[1]

        if text:
            split_nodes.append(TextNode(text, "text"))

        new_nodes.extend(split_nodes)
    return new_nodes


def text_to_textnodes(text):
    node = TextNode(text, text_type="text")
    nodes = split_nodes_delimiter([node], delimiter="**", text_type="bold")
    nodes = split_nodes_delimiter(nodes, delimiter="*", text_type="italic")
    nodes = split_nodes_delimiter(nodes, delimiter="`", text_type="code")
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def markdown_to_blocks(markdown):
    return [b.strip() for b in markdown.split("\n\n") if b.strip()]


def block_to_block_type(block):
    if re.findall(r"^#{1,6} .+", block):
        return "heading"
    if re.findall(r"^`{3}.+`{3}$", block):
        return "code"
    if re.findall(r"^> .+", block):
        return "quote"
    if is_unordered_list(block):
        return "unordered_list"
    if is_ordered_list(block):
        return "ordered_list"
    return "paragraph"


def is_unordered_list(block):
    lines = [l for l in block.split("\n") if l]

    for line in lines:
        pattern = r"^(\*|-) .+"
        temp = re.findall(pattern, line)
        if not temp:
            return False

    return True


def is_ordered_list(block):
    lines = [l for l in block.split("\n") if l]

    for i, line in enumerate(lines):
        pattern = "^" + str(i + 1) + r"\. .+"
        temp = re.findall(pattern, line)
        if not temp:
            return False

    return True


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)

    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case "heading":
                hashtags_before_text = block.split(" ")[0]
                num_of_hashtags = len(hashtags_before_text)
                text_after_hashtags = block[num_of_hashtags + 1 :]
                children.append(
                    ParentNode(
                        tag=f"h{num_of_hashtags}",
                        children=text_to_children(text_after_hashtags),
                    )
                )
            case "code":
                children.append(
                    ParentNode(
                        tag="pre",
                        children=ParentNode(
                            tag="code", children=text_to_children(block[3:-3])
                        ),
                    )
                )
            case "quote":
                children.append(
                    ParentNode(
                        tag="blockquote",
                        children=text_to_children(block[2:]),
                    )
                )
            case "unordered_list":
                children.append(
                    ParentNode(
                        tag="ul",
                        children=[
                            ParentNode(tag="li", children=text_to_children(text[2:]))
                            for text in block.split("\n")
                        ],
                    )
                )
            case "ordered_list":
                children.append(
                    ParentNode(
                        tag="ol",
                        children=[
                            ParentNode(tag="li", children=text_to_children(text[3:]))
                            for text in block.split("\n")
                        ],
                    )
                )
            case _:
                children.append(ParentNode(tag="p", children=text_to_children(block)))

    return ParentNode(tag="div", children=children)


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(text_node) for text_node in text_nodes]


if __name__ == "__main__":
    main()
