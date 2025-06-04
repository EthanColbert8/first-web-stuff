import re

from .textnode import TextType, TextNode

image_pattern = re.compile(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)")
link_pattern = re.compile(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)")

def extract_markdown_images(text):
    return image_pattern.findall(text)

def extract_markdown_links(text):
    return link_pattern.findall(text)

def split_nodes_links_or_images(old_nodes: list, image: bool) -> list:
    new_nodes = []
    for node in old_nodes:
        if (not isinstance(node, TextNode)):
            raise TypeError(f"Expected TextNode, got {type(node)}")
        
        if (node.text_type != TextType.TEXT):
            new_nodes.append(node)
            continue
        
        if image:
            pattern_matches = extract_markdown_images(node.text)
        else:
            pattern_matches = extract_markdown_links(node.text)
        
        if (not pattern_matches):
            new_nodes.append(node)
            continue
        
        remaining_text = node.text
        for match in pattern_matches:
            text, url = match

            if image:
                sections = remaining_text.split(f"![{text}]({url})", 1)
            else:
                sections = remaining_text.split(f"[{text}]({url})", 1)
        
            if len(sections) != 2:
                raise ValueError(f"Problem splitting text containing {"images" if image else "links"}.")
            
            if (sections[0] != ""):
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            
            if image:
                new_nodes.append(TextNode(text, TextType.IMAGE, url))
            else:
                new_nodes.append(TextNode(text, TextType.LINK, url))
            
            remaining_text = sections[1]
        
        if (remaining_text != ""):
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    
    return new_nodes

def split_nodes_images(old_nodes: list) -> list:
    return split_nodes_links_or_images(old_nodes, True)

def split_nodes_links(old_nodes: list) -> list:
    return split_nodes_links_or_images(old_nodes, False)

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
