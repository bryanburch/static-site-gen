from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        if children is None:
            children = []
        if not isinstance(children, list):
            children = [children]
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("ParentNode tag attribute cannot be None.")

        if not self.children:
            raise ValueError("ParentNode children attribute cannot be None.")

        props = self.props if self.props else ""
        html = f"<{self.tag}{props}>"
        for node in self.children:
            html += node.to_html()
        html += f"</{self.tag}>"
        return html
