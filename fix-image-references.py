#!/usr/bin/env python3
import re, os
from pathlib import Path

WEBSITE = Path(__file__).parent / 'website'
IMG_DIR = WEBSITE / 'images'

# compute hyphenified name from actual name with spaces

def hyphenify(name):
    base, ext = os.path.splitext(name)
    # remove parentheses
    base = re.sub(r'[()]', '', base)
    # replace whitespace with hyphen
    base = re.sub(r'\s+', '-', base)
    # collapse multiple hyphens
    base = re.sub(r'-+', '-', base)
    return base + ext

# build mapping from wrong->correct for files with spaces
mapping = {}
for f in IMG_DIR.iterdir():
    if ' ' in f.name or '(' in f.name or ')' in f.name:
        wrong = hyphenify(f.name)
        if wrong != f.name:
            mapping[wrong] = f.name

print('Mapping of hyphenified to actual:')
for k,v in mapping.items():
    print(k, '->', v)

# replace occurrences in all html/css

def replace_in_file(path):
    text = path.read_text(encoding='utf-8')
    orig = text
    for wrong, actual in mapping.items():
        text = text.replace(wrong, actual)
    if text != orig:
        path.write_text(text, encoding='utf-8')
        print('Updated', path.relative_to(WEBSITE))

for ext in ['*.html','*.css']:
    for p in WEBSITE.rglob(ext):
        replace_in_file(p)

print('Done replacements.')
