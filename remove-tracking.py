#!/usr/bin/env python3
import os
import re

WEBSITE_DIR = os.path.join(os.path.dirname(__file__), 'website')

SNIPPET_REGEX = re.compile(r'<script src="(?:\.\./)*js/tracking\.js"></script>\s*', re.IGNORECASE)


def remove_tracking_from_file(filepath):
    rel = os.path.relpath(filepath, WEBSITE_DIR)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    new_content = re.sub(SNIPPET_REGEX, '', content)
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"✓ removed tracking from {rel}")
    else:
        print(f"- no snippet found in {rel}")

if __name__ == '__main__':
    for root, dirs, files in os.walk(WEBSITE_DIR):
        for file in files:
            if file.endswith('.html'):
                remove_tracking_from_file(os.path.join(root, file))
