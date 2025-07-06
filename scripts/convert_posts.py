#!/usr/bin/env python3
"""
Convert Jekyll-style posts to Astro content collection format.

This script converts posts from the date-prefixed filename format with Jekyll frontmatter
to the Astro content collection format with proper schema.
"""

import os
import re
from pathlib import Path
from datetime import datetime


def extract_date_from_filename(filename):
    """Extract date from filename like '2024-12-07-post-title.md'."""
    match = re.match(r'(\d{4}-\d{2}-\d{2})-(.+)\.md$', filename)
    if match:
        date_str, slug = match.groups()
        return date_str, slug
    return None, None


def convert_frontmatter(frontmatter_content, date_str):
    """Convert Jekyll frontmatter to Astro content collection format."""
    lines = frontmatter_content.strip().split('\n')
    
    # Extract existing fields
    title = ""
    tags = []
    
    for line in lines:
        if line.startswith('title:'):
            title = line.split('title:', 1)[1].strip()
        elif line.startswith('tags:'):
            # Parse tags array: [poetry, essay] or [economics, essay]
            tags_str = line.split('tags:', 1)[1].strip()
            # Remove brackets and split by comma
            tags_str = tags_str.strip('[]')
            if tags_str:
                tags = [tag.strip() for tag in tags_str.split(',')]
    
    # Create new frontmatter
    new_frontmatter = f"""---
title: {title}
date: {date_str}"""
    
    if tags:
        tags_formatted = '[' + ', '.join([f'"{tag}"' for tag in tags]) + ']'
        new_frontmatter += f"\ntags: {tags_formatted}"
    
    new_frontmatter += "\n---"
    
    return new_frontmatter


def clean_content(content):
    """Clean up post content for Astro."""
    # Remove Jekyll-specific syntax
    # Remove {: .box-note} style annotations
    content = re.sub(r'\{: \.[\w-]+\}', '', content)
    
    # Clean up extra line breaks and formatting
    content = re.sub(r'<br><br><br>', '\n\n', content)
    content = re.sub(r'<br>', '\n', content)
    
    # Remove Jekyll script tags that might not work in Astro
    content = re.sub(r'<script[^>]*src="https://cdn\.mathjax\.org[^"]*"[^>]*></script>', '', content)
    
    # Clean up multiple consecutive line breaks
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    return content.strip()


def convert_post_file(file_path):
    """Convert a single post file."""
    filename = file_path.name
    date_str, slug = extract_date_from_filename(filename)
    
    if not date_str or not slug:
        print(f"Warning: Could not parse date from filename: {filename}")
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split frontmatter and content
        if not content.startswith('---'):
            print(f"Warning: No frontmatter found in {filename}")
            return False
        
        parts = content.split('---', 2)
        if len(parts) < 3:
            print(f"Warning: Invalid frontmatter format in {filename}")
            return False
        
        frontmatter_content = parts[1]
        post_content = parts[2]
        
        # Convert frontmatter
        new_frontmatter = convert_frontmatter(frontmatter_content, date_str)
        
        # Clean content
        cleaned_content = clean_content(post_content)
        
        # Create new filename (remove date prefix)
        new_filename = slug + '.md'
        
        # Write the converted file
        new_content = new_frontmatter + '\n\n' + cleaned_content
        
        with open(file_path.parent / new_filename, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        # Remove old file if new filename is different
        if new_filename != filename:
            os.remove(file_path)
        
        print(f"Converted: {filename} -> {new_filename}")
        return True
        
    except Exception as e:
        print(f"Error converting {filename}: {e}")
        return False


def main():
    # Get the posts directory
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    posts_dir = project_root / "src" / "content" / "posts"
    
    if not posts_dir.exists():
        print(f"Error: Posts directory not found: {posts_dir}")
        return
    
    print(f"Converting posts in {posts_dir}")
    
    converted_count = 0
    error_count = 0
    
    # Process all .md files
    for md_file in posts_dir.glob("*.md"):
        # Skip files that don't have date prefix (already converted)
        if not re.match(r'\d{4}-\d{2}-\d{2}-', md_file.name):
            print(f"Skipping already converted file: {md_file.name}")
            continue
            
        if convert_post_file(md_file):
            converted_count += 1
        else:
            error_count += 1
    
    print(f"\nConversion complete!")
    print(f"Converted: {converted_count} posts")
    print(f"Errors: {error_count} posts")


if __name__ == "__main__":
    main()