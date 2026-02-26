#!/usr/bin/env python3
import os
import re

WEBSITE_DIR = os.path.join(os.path.dirname(__file__), 'website')

TRACK_SNIPPET_TEMPLATE = '<script src="{path}"></script>'


def add_tracking_to_file(filepath):
    rel = os.path.relpath(filepath, WEBSITE_DIR)
    # compute depth: number of directories between website and file
    depth = rel.count(os.sep)  # 'dir/index.html' => depth=1
    # prefix relative path from file to website root
    prefix = '../' * depth
    path = prefix + 'js/tracking.js'
    snippet = TRACK_SNIPPET_TEMPLATE.format(path=path)

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if snippet in content:
        print(f"- tracking already present in {rel}")
        return
    # insert before </body>
    new_content = re.sub(r'(</body>)', snippet + '\n\1', content, flags=re.IGNORECASE)
    if new_content == content:
        print(f"! could not find </body> in {rel}")
        return
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"✓ added tracking to {rel}")


if __name__ == '__main__':
    for root, dirs, files in os.walk(WEBSITE_DIR):
        for file in files:
            if file.endswith('.html'):
                add_tracking_to_file(os.path.join(root, file))
