#!/usr/bin/env python3
import os
import re
from pathlib import Path

WEBSITE_DIR = os.path.join(os.path.dirname(__file__), 'website')

def fix_relative_paths():
    """Fix relative paths in all refactored HTML files"""
    
    # Find all index.html files that were refactored
    for root, dirs, files in os.walk(WEBSITE_DIR):
        if 'index.html' in files:
            file_path = os.path.join(root, 'index.html')
            rel_from_website = os.path.relpath(file_path, WEBSITE_DIR)
            depth = rel_from_website.count(os.sep)
            
            # Skip if this is the root index.html
            if depth == 0:
                continue
            
            # Read file
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original = content
            
            # For files that were moved from subdirectories (depth >= 1)
            # Update relative paths to add an extra ../
            # Pattern: href="..." or src="..." that have relative paths
            def update_url(match):
                before = match.group(1)  # href=" or src="
                url = match.group(2)     # the URL
                after = match.group(3)   # the closing "
                
                # Skip absolute paths, external URLs, mailto, and anchors
                if url.startswith(('http://', 'https://', 'mailto:', '/', '#', 'data:')):
                    return match.group(0)
                
                # For relative paths, add ../ prefix if going up, then others
                if url.startswith('../'):
                    # Count existing ../ prefixes
                    prefix_count = 0
                    temp = url
                    while temp.startswith('../'):
                        prefix_count += 1
                        temp = temp[3:]
                    
                    # Add one more ../ since file is now one level deeper
                    new_url = '../' + url
                    return f'{before}{new_url}{after}'
                elif not url.startswith('./'):
                    # For non-relative paths like css/, images/, add ../
                    new_url = '../' + url
                    return f'{before}{new_url}{after}'
                
                return match.group(0)
            
            # Apply the fix
            content = re.sub(
                r'((?:href|src)=")([^"]+)(")',
                update_url,
                content
            )
            
            # Write back if changed
            if content != original:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✓ Fixed paths: {rel_from_website}")
            else:
                print(f"\\ Skipped (root level or already correct): {rel_from_website}")

if __name__ == '__main__':
    print("Fixing relative paths in refactored HTML files...\n")
    fix_relative_paths()
    print("\n✓ Path fix complete!")
