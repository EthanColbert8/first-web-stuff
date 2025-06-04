from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = 1
    HEADING = 2
    CODE = 3
    QUOTE = 4
    UNORDERED_LIST = 5
    ORDERED_LIST = 6

def block_to_blocktype(block: str) -> BlockType:
    if re.fullmatch(r"\A```(.*\n?)*```\Z", block, flags=re.M):
        return BlockType.CODE
    
    if re.fullmatch(r"^(>.*\n?)+", block, flags=re.M):
        return BlockType.QUOTE
    
    if re.fullmatch(r"^(- .*\n?)+", block, flags=re.M):
        return BlockType.UNORDERED_LIST
    
    if re.fullmatch(r"^(\d+\. .*\n?)+", block, flags=re.M):
        return BlockType.ORDERED_LIST
    
    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING
    
    return BlockType.PARAGRAPH

def markdown_to_blocks(markdown: str) -> list:
    blocks = []

    lines = markdown.split("\n\n")
    for line in lines:
        if (line == "" or line.isspace()):
            continue
        
        blocks.append(line.strip())
    
    return blocks