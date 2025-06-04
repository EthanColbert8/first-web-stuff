from . import parser

if (__name__ == "__main__"):
    markdown1 = "Here's some text surrounding a [link](https://example.com) and an [extra link](https://not_a_website.com) for good measure."
    markdown2 = "Here's some text surrounding a ![image](https://example.com/image.png) and an ![]() for good measure."

    print(parser.extract_markdown_links(markdown1))
    print(parser.extract_markdown_images(markdown2))
