#imports here

class HTMLNode:
    def __init__(self, tag: str = None, value: str = None, children: list = None, props: dict = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self) -> str:
        raise NotImplementedError("Child classes should override this method.")
    
    def props_to_html(self) -> str:
        if (not self.props):
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
        
