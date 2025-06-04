from . import blockparser

if (__name__ == "__main__"):
    markdown1 = "## This is a heading."
    markdown2 = "```Here's some\ncode()\nwith multiple lines\nand symbols[]```"
    #markdown2 = "- This is an\n- unordered list"

    print(blockparser.block_to_blocktype(markdown1))
    print(blockparser.block_to_blocktype(markdown2))
