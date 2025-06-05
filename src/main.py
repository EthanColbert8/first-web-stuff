import os
import shutil
import sys

from .MDtoHTML import markdown_to_html_node

def copy_tree(src: str, dest: str):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.mkdir(dest)
    
    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dest_path = os.path.join(dest, item)
        
        if os.path.isfile(src_path):
            shutil.copy(src_path, dest_path)
        else:
            copy_tree(src_path, dest_path)

def extract_title(markdown: str) -> str:
    lines = markdown.split("\n")

    title_line = None
    for line in lines:
        if line.startswith("# "):
            title_line = line
            break
    
    if title_line is None:
        raise ValueError("No title found in the markdown content.")
    
    return title_line.lstrip("# ").strip()

def generate_page(src: str, template: str, dest: str, basepath: str = "/"):
    print(f"Generating page from {src} to {dest} using {template}")

    with open(src, "r") as src_file:
        markdown_content = src_file.read()
    
    title = extract_title(markdown_content)
    
    if (not os.path.isfile(template)):
        raise ValueError(f"Template file {template} does not exist.")
    with open(template, "r") as template_file:
        template_content = template_file.read()
    
    html_content = markdown_to_html_node(markdown_content).to_html()

    page_content = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_content).replace("href=\"/", f"href=\"{basepath}").replace("src=\"/", f"src=\"{basepath}")

    with open(dest, "w") as dest_file:
        dest_file.write(page_content)

def generate_pages_recursive(src: str, template: str, dest: str, basepath: str = "/"):
    if (not os.path.isdir(src)):
        raise ValueError(f"Source {src} is not a directory.")
    os.makedirs(dest, exist_ok=True)

    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dest_path = os.path.join(dest, item)

        if os.path.isfile(src_path):
            dest_path = dest_path.replace(".md", ".html")
            generate_page(src_path, template, dest_path, basepath)
        else:
            generate_pages_recursive(src_path, template, dest_path, basepath)

if (__name__ == "__main__"):
    if (len(sys.argv) > 2):
        print("Usage: python -m src.main [basepath]")
        sys.exit(1)
    
    basepath = "/"
    if (len(sys.argv) == 2):
        basepath = sys.argv[1]
    
    build_dir = "docs"

    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)
    copy_tree("static", build_dir)

    generate_pages_recursive("content", "template.html", build_dir, basepath)
