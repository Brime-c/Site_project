class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        prop_string = ""
        if self.props:    
            for key, value in self.props.items():
                prop_string += f' {key}="{value}"'
        return prop_string
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    def __eq__(self,other):
        if isinstance(other, HTMLNode):
            return self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props
        return False
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, children=None, props=props)
    def to_html(self):
        if not self.value:
            raise ValueError("all leaf nodes must have a value")
        if self.tag == None:
            return self.value
        if not self.props:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)
    def to_html(self):
        if not self.tag:
            raise ValueError("Tag not found")
        if not self.children:
            raise ValueError("Children not found")
        children_htmlstring = ""
        for c in self.children:
            string = c.to_html()
            children_htmlstring += string
        return f"<{self.tag}>{children_htmlstring}</{self.tag}>"
    

    