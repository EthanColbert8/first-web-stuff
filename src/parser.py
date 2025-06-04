from .textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes: list, delimiter: str, text_type: TextType) -> list:
    new_nodes = []
    for node in old_nodes:
        if (not isinstance(node, TextNode)):
            raise TypeError(f"Expected TextNode, got {type(node)}")
        
        if (node.text_type != TextType.TEXT):
            new_nodes.append(node)
            continue
        
        string_parts = node.text.split(delimiter)

        # If there's only one part, no delimiter was found and we're done
        if (len(string_parts) == 1):
            new_nodes.append(node)
            continue

        # If there are an even number of parts, then there's an odd number of delimiters,
        # meaning one is unmatched.
        if (len(string_parts) % 2 != 1):
            raise ValueError("Unmatched delimiter found.")
        
        for idx, part in enumerate(string_parts):
            if (part == ""):
                continue
            
            # Even indices are text parts, odd ones are parts set by delimiters.
            if (idx % 2 == 0):
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))
    
    return new_nodes
