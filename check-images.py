#!/usr/bin/env python3
import os, re
from pathlib import Path

WEBSITE_DIR = Path(__file__).parent / 'website'

# pattern for src/href referencing images folder
pattern = re.compile(r'"(\.\./)*images/([^"]+)"')

missing = {}

for i, html in enumerate(WEBSITE_DIR.rglob('*.html')):
    if i % 50 == 0:
        print(f"scanning {i} files, current {html}")
    try:
        text = html.read_text(encoding='utf-8')
    except Exception as e:
        print(f"could not read {html}: {e}")
        continue
    for m in pattern.finditer(text):
        relpath = m.group(0).strip('"')
        # resolve relative path using pathlib
        candidate_path = (Path(html.parent) / relpath).resolve()
        if not candidate_path.exists():
            # extract filename portion after images/
            try:
                fname = relpath.split('images/')[1]
            except IndexError:
                fname = relpath
            missing.setdefault(fname, []).append(str(html.relative_to(WEBSITE_DIR)))

# now print missing files and candidate fixes
for fname, pages in missing.items():
    print(f"MISSING: {fname} referenced in {len(pages)} files")
    # look for candidate in images directory by replacing hyphen before digits with space
    candidate = None
    # pattern to replace last hyphen-group before extension to space
    base, ext = os.path.splitext(fname)
    # try simple substitution rules
    if '-' in base:
        cand = base.replace('-', ' ') + ext
        if (WEBSITE_DIR / 'images' / cand).exists():
            candidate = cand
    if candidate:
        print(f"  -> has candidate {candidate}")
    else:
        # try replace multiple hyphens with spaces?  maybe pattern of digits
        print("  -> no simple candidate")
    #list pages
    for p in pages[:5]:
        print("    ", p)

# additionally list filenames with spaces in images dir
dirs = WEBSITE_DIR / 'images'
spaced = [f for f in dirs.iterdir() if ' ' in f.name]
print('\nFILES WITH SPACES:')
for f in spaced:
    print(' ', f.name)