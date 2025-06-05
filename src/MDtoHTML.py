from . import textnode
from . import htmlnode
from . import parser
from . import blockparser

def markdown_to_html_node(markdown: str) -> htmlnode.HTMLNode:
    """
    Convert a markdown string to an HTML parent node. The node will contain
    all of the contents of the original markdown as a tree,of which the
    returned node is the root.
    """
    md_blocks = blockparser.markdown_to_blocks(markdown)

    nodes = []
    for md_block in md_blocks:
        block_type = blockparser.block_to_blocktype(md_block)
        match block_type:
            case blockparser.BlockType.HEADING:
                nodes.append(handle_heading(md_block))
            case blockparser.BlockType.CODE:
                nodes.append(handle_code(md_block))
            case blockparser.BlockType.QUOTE:
                nodes.append(handle_quote(md_block))
            case blockparser.BlockType.UNORDERED_LIST:
                nodes.append(handle_ul(md_block))
            case blockparser.BlockType.ORDERED_LIST:
                nodes.append(handle_ol(md_block))
            case blockparser.BlockType.PARAGRAPH:
                nodes.append(handle_paragraph(md_block))
            case _:
                raise Exception(f"Problem parsing markdown block: {md_block}")

    return htmlnode.ParentNode("div", nodes)

def handle_heading(text: str) -> htmlnode.HTMLNode:
    hashtags = text.split(" ")[0]
    content = text.lstrip("# ")

    tag = f"h{len(hashtags)}"
    children = get_childnodes_from_text(content)

    return htmlnode.ParentNode(tag, children)

def handle_code(text: str) -> htmlnode.HTMLNode:
    code_content = text.strip("`").lstrip("\n")
    node = textnode.TextNode(code_content, textnode.TextType.CODE)
    code_node = textnode.textnode_to_html(node)
    return htmlnode.ParentNode("pre", [code_node])

def handle_quote(text: str) -> htmlnode.HTMLNode:
    quote_lines = [line.lstrip("> ") for line in text.split("\n")]
    quote_text = "\n".join(quote_lines)

    children = get_childnodes_from_text(quote_text)

    return htmlnode.ParentNode("blockquote", children)

def handle_ul(text: str) -> htmlnode.HTMLNode:
    items = [item.lstrip("- ") for item in text.split("\n")]

    child_nodes = []
    for item in items:
        child_nodes.append(htmlnode.ParentNode("li", get_childnodes_from_text(item)))
    
    return htmlnode.ParentNode("ul", child_nodes)

def handle_ol(text: str) -> htmlnode.HTMLNode:
    items = [item.lstrip("1234567890. ") for item in text.split("\n")]

    child_nodes = []
    for item in items:
        child_nodes.append(htmlnode.ParentNode("li", get_childnodes_from_text(item)))
    
    return htmlnode.ParentNode("ol", child_nodes)

def handle_paragraph(text: str) -> htmlnode.HTMLNode:
    oneline_text = text.replace("\n", " ")
    children = get_childnodes_from_text(oneline_text)
    return htmlnode.ParentNode("p", children)

def get_childnodes_from_text(text: str) -> list:
    textnodes = parser.text_to_textnodes(text)
    return [textnode.textnode_to_html(node) for node in textnodes]
    