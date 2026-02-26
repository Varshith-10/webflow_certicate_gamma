#!/usr/bin/env python3
import os

WEBSITE_DIR = os.path.join(os.path.dirname(__file__), 'website')


def ensure_body_close(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    has_close = any('</body>' in line.lower() for line in lines)
    if has_close:
        return False
    # find last occurrence of </html> and insert </body> before it
    out_lines = []
    inserted = False
    for line in lines:
        if not inserted and '</html>' in line.lower():
            out_lines.append('    </body>\n')
            inserted = True
        out_lines.append(line)
    if inserted:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(out_lines)
        return True
    return False

if __name__ == '__main__':
    for root, dirs, files in os.walk(WEBSITE_DIR):
        for file in files:
            if file.endswith('.html'):
                full = os.path.join(root, file)
                if ensure_body_close(full):
                    print(f"✓ added closing body to {os.path.relpath(full, WEBSITE_DIR)}")
