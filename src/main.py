import os
import shutil

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

if (__name__ == "__main__"):
    copy_tree("static", "public")
