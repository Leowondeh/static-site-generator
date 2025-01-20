class HTMLNode:
    def __init__(self, tag: str = None, value: str = None, children: list = None, properties: dict = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.properties = properties

    def to_html(self):
        raise NotImplementedError

    def properties_to_html(self) -> str:
        if self.properties is None:
            return ""
        converted_html = " " # start with a space to conform with HTML formatting
        for property, value in self.properties.items():
            converted_html += f'{property}="{value}" '
        
        return converted_html[:-1] # except last space
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.properties})"

class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, properties: dict = None):
        super().__init__(tag, value, None, properties)
    
    def to_html(self) -> str:
        if self.value == None:
            raise ValueError('Leaf nodes must have a value')
        elif self.tag == None:
            return self.value
        
        return f"<{self.tag}{self.properties_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.properties})"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children=None, properties=None):
        if children is None:
            children = []
        super().__init__(tag, None, children, properties)
    
    def to_html(self) -> str:
        if self.tag == None or self.tag == '':
            raise ValueError('ParentNode requires a tag')
        if self.children == None or self.children == []:
            raise ValueError('ParentNode requires at least one child')
        
        children_html = ""

        for child in self.children:
            children_html += child.to_html()
        
        return f"<{self.tag}{self.properties_to_html()}>{children_html}</{self.tag}>"