#!/usr/bin/env python3
import os
import re

WEBSITE_DIR = os.path.join(os.path.dirname(__file__), 'website')

def fix_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    orig = content
    # replace ../../css with ../css, ../../images with ../images, ../../js with ../js
    content = re.sub(r"\.\./\.\./(css|images|js)/", r"../\1/", content)
    # also fix ../../css and others without trailing slash
    content = re.sub(r"\.\./\.\./(css|images|js)", r"../\1", content)
    if content != orig:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ fixed top-level paths in {os.path.relpath(path, WEBSITE_DIR)}")
    else:
        print(f"- no changes needed for {os.path.relpath(path, WEBSITE_DIR)}")

if __name__ == '__main__':
    for root, dirs, files in os.walk(WEBSITE_DIR):
        for file in files:
            if file == 'index.html':
                relpath = os.path.relpath(os.path.join(root, file), WEBSITE_DIR)
                if relpath.count(os.sep) == 1:  # depth 1
                    fix_file(os.path.join(root, file))
