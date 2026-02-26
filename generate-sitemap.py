#!/usr/bin/env python3
import os
from pathlib import Path

WEBSITE_DIR = Path(__file__).parent / 'website'
BASE_URL = 'https://certificates.ccbp.in'

urls = []
for path in WEBSITE_DIR.rglob('index.html'):
    rel = path.relative_to(WEBSITE_DIR)
    # skip root index is ''
    parts = rel.parts[:-1]  # drop index.html
    if parts:
        url = '/'.join(parts) + '/'
    else:
        url = ''
    urls.append(url)

# also include 404? often not.

# construct xml
lines = ['<?xml version="1.0" encoding="UTF-8"?>',
         '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for u in sorted(urls):
    lines.append('  <url>')
    lines.append(f'    <loc>{BASE_URL}/{u}</loc>')
    lines.append('  </url>')
lines.append('</urlset>')

sitemap_path = WEBSITE_DIR / 'sitemap.xml'
with open(sitemap_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))
print(f'Generated {sitemap_path} with {len(urls)} entries')
