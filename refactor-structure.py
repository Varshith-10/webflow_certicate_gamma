#!/usr/bin/env python3
import os
import shutil
import re
from pathlib import Path

WEBSITE_DIR = os.path.join(os.path.dirname(__file__), 'website')
EXCLUDE_FILES = ['index.html', '404.html']

def get_all_html_files(directory=WEBSITE_DIR, prefix=''):
    """Get all HTML files recursively"""
    files = []
    
    for item in os.listdir(directory):
        full_path = os.path.join(directory, item)
        rel_path = os.path.join(prefix, item) if prefix else item
        
        if os.path.isdir(full_path):
            if item not in ['node_modules', '.git']:
                files.extend(get_all_html_files(full_path, rel_path))
        elif item.endswith('.html'):
            files.append({
                'name': item,
                'dir': directory,
                'relative_path': rel_path.replace(os.sep, '/'),
                'full_path': full_path,
                'should_refactor': item not in EXCLUDE_FILES
            })
    
    return files

def get_depth(relative_path):
    """Get depth of a file (how many directories deep from website root)"""
    return relative_path.count('/')

def update_relative_paths(content, old_depth, new_depth):
    """Update relative paths in HTML content"""
    depth_diff = new_depth - old_depth
    
    if depth_diff == 0:
        return content
    
    # Build the prefix to add
    if depth_diff > 0:
        prefix_to_add = '../' * depth_diff
        # Match href="..." or src="..." that don't start with http, https, mailto, or #
        pattern = r'((?:href|src)=")(?!(?:https?:|mailto:|#|/))([^"]+)(")'
        
        def replacer(match):
            before = match.group(1)
            url = match.group(2)
            after = match.group(3)
            # Don't add prefix if already has ../
            if not url.startswith('../'):
                return f'{before}{prefix_to_add}{url}{after}'
            return match.group(0)
        
        return re.sub(pattern, replacer, content)
    
    return content

def refactor_structure():
    """Refactor file structure"""
    all_files = get_all_html_files()
    files_to_refactor = [f for f in all_files if f['should_refactor']]
    
    print(f"Found {len(all_files)} HTML files, refactoring {len(files_to_refactor)}...\n")
    
    file_moves = {}
    
    # Step 1: Create folders and move/update files
    for file in sorted(files_to_refactor, key=lambda x: x['relative_path']):
        folder_name = os.path.splitext(file['name'])[0]
        new_folder_path = os.path.join(file['dir'], folder_name)
        new_file_path = os.path.join(new_folder_path, 'index.html')
        
        # Create folder
        if not os.path.exists(new_folder_path):
            os.makedirs(new_folder_path, exist_ok=True)
            print(f"✓ Created folder: {os.path.relpath(new_folder_path, WEBSITE_DIR)}")
        
        # Read and update content
        with open(file['full_path'], 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Calculate depth difference
        old_depth = get_depth(file['relative_path'])
        new_depth = get_depth(os.path.relpath(new_file_path, WEBSITE_DIR).replace(os.sep, '/'))
        
        content = update_relative_paths(content, old_depth, new_depth)
        
        # Write to new location
        with open(new_file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        old_rel_path = os.path.relpath(file['full_path'], WEBSITE_DIR)
        new_rel_path = os.path.relpath(new_file_path, WEBSITE_DIR)
        print(f"✓ Migrated: {old_rel_path} → {new_rel_path}")
        
        # Track the move
        old_key = file['relative_path'].replace(os.sep, '/')
        new_folder_rel = os.path.relpath(new_folder_path, WEBSITE_DIR).replace(os.sep, '/')
        file_moves[old_key] = new_folder_rel
        
        # Delete original file
        os.remove(file['full_path'])
        print(f"✓ Deleted: {old_rel_path}\n")
    
    print("\n✓ Structure refactoring complete!")
    print("\nFile movements:")
    for old, new_folder in sorted(file_moves.items()):
        print(f"  {old} → {new_folder}/index.html")

# Run refactoring
try:
    refactor_structure()
except Exception as error:
    print(f'Error during refactoring: {error}')
    import traceback
    traceback.print_exc()
    exit(1)
