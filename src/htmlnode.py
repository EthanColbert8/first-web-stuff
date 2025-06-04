class HTMLNode:
    def __init__(self, tag: str = None, value: str = None, children: list = None, props: dict = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self) -> str:
        raise NotImplementedError("Child classes should override this method.")
    
    def props_to_html(self) -> str:
        if (self.props is None):
            return ""
        
        string = ""
        for key, value in self.props.items():
            string += f" {key}=\"{value}\""
        
        return string
    
    def __repr__(self) -> str:
        attributes = []
        
        if self.tag:
            attributes.append(f"tag=\"{self.tag}\"")
        
        if self.value:
            attributes.append(f"value=\"{self.value}\"")
        
        if self.children:
            attributes.append(f"children=[{", ".join([repr(child) for child in self.children])}]")
        
        if self.props:
            props_str = ", ".join([f"\"{key}\": \"{value}\"" for key, value in self.props.items()])
            attributes.append(f"props={{{props_str}}}")
        
        return f"HTMLNode({', '.join(attributes)})"
        
class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props: dict = None):
        super().__init__(tag, value, props=props)
    
    def to_html(self) -> str:
        if (self.value is None):
            raise ValueError("Leaf nodes must have a value.")
        
        if (self.tag is None):
            return self.value

        props_html = self.props_to_html()

        return f"<{self.tag}{props_html}>{self.value}</{self.tag}>"
    
class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list, props: dict = None):
        super().__init__(tag, children=children, props=props)
    
    def to_html(self) -> str:
        if (self.tag is None):
            raise ValueError("Parent nodes must have a tag.")
        
        if (self.children is None):
            raise ValueError("Parent nodes must have children.")

        props_html = self.props_to_html()

        children_html = [child.to_html() for child in self.children]

        return f"<{self.tag}{props_html}>{"".join(children_html)}</{self.tag}>"
