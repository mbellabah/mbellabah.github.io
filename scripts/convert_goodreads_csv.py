#!/usr/bin/env python3
"""
Convert Goodreads CSV export to Astro content collection markdown files.

Usage:
    python scripts/convert_goodreads_csv.py src/data/books/goodreads_library_export.csv

This script converts a Goodreads CSV export into individual markdown files
for the Astro books content collection.
"""

import csv
import os
import sys
import re
from datetime import datetime
from pathlib import Path


def clean_filename(title):
    """Convert book title to a clean filename."""
    # Remove special characters and replace spaces with hyphens
    filename = re.sub(r'[^\w\s-]', '', title.lower())
    filename = re.sub(r'[-\s]+', '-', filename)
    return filename.strip('-')


def parse_date(date_str):
    """Parse Goodreads date format (YYYY/MM/DD) to ISO format."""
    if not date_str or date_str.strip() == '':
        return None
    
    try:
        # Goodreads format: YYYY/MM/DD
        date_obj = datetime.strptime(date_str.strip(), '%Y/%m/%d')
        return date_obj.strftime('%Y-%m-%d')
    except ValueError:
        print(f"Warning: Could not parse date '{date_str}'")
        return None


def extract_year_from_shelves(shelves):
    """Extract year from shelf names like 'read-2024'."""
    if not shelves:
        return None
    
    # Look for patterns like "read-YYYY" or "read YYYY"
    import re
    year_pattern = r'read[-\s](\d{4})'
    match = re.search(year_pattern, shelves.lower())
    
    if match:
        year = int(match.group(1))
        # Sanity check: reasonable reading years
        current_year = datetime.now().year
        if 1900 <= year <= current_year:
            return year
    
    return None


def determine_read_date(date_read_str, shelves):
    """Determine read date from explicit date or shelf information."""
    # First try explicit date
    explicit_date = parse_date(date_read_str)
    if explicit_date:
        return explicit_date, False  # (date, is_approximate)
    
    # Try to extract year from shelves
    year = extract_year_from_shelves(shelves)
    if year:
        # Use June 30th as a middle-of-year estimate
        return f"{year}-06-30", True  # (date, is_approximate)
    
    # No date information available
    return "Unknown", False


def clean_review_text(review_text):
    """Clean up review text for markdown."""
    if not review_text:
        return ""
    
    # Remove HTML tags
    review_text = re.sub(r'<[^>]+>', '', review_text)
    
    # Replace HTML entities
    review_text = review_text.replace('&quot;', '"')
    review_text = review_text.replace('&amp;', '&')
    review_text = review_text.replace('&lt;', '<')
    review_text = review_text.replace('&gt;', '>')
    
    # Clean up extra whitespace
    review_text = re.sub(r'\s+', ' ', review_text).strip()
    
    return review_text


def determine_genre(shelves, title, author):
    """Determine genre from Goodreads shelves or make educated guess."""
    if not shelves:
        return "Unknown"  # Default
    
    shelves_lower = shelves.lower()
    
    # Genre mapping based on common Goodreads shelves
    genre_keywords = {
        'non-fiction': 'Non-fiction',
        'nonfiction': 'Non-fiction',
        'biography': 'Biography',
        'memoir': 'Memoir',
        'history': 'History',
        'philosophy': 'Philosophy',
        'science': 'Science',
        'business': 'Business',
        'psychology': 'Psychology',
        'self-help': 'Self-help',
        'fantasy': 'Fantasy',
        'sci-fi': 'Science Fiction',
        'science-fiction': 'Science Fiction',
        'mystery': 'Mystery',
        'thriller': 'Thriller',
        'romance': 'Romance',
        'literary': 'Literary Fiction',
        'classic': 'Classic',
        'poetry': 'Poetry',
    }
    
    for keyword, genre in genre_keywords.items():
        if keyword in shelves_lower:
            return genre
    
    # If no clear genre from shelves, default to Unknown
    return "Unknown"


def convert_csv_to_markdown(csv_file_path, output_dir):
    """Convert Goodreads CSV to markdown files."""
    
    # Ensure output directory exists
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    converted_count = 0
    skipped_count = 0
    approximate_count = 0
    unknown_count = 0
    
    with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            title = row.get('Title', '').strip()
            author = row.get('Author', '').strip()
            
            if not title or not author:
                print("Warning: Skipping book with missing title or author")
                skipped_count += 1
                continue
            
            # Clean up title (remove quotes and extra formatting)
            title = re.sub(r'^"(.*)"$', r'\1', title)
            
            # Determine read date (explicit, from shelves, or unknown)
            shelves = row.get('Bookshelves', '')
            date_read_str = row.get('Date Read', '')
            date_completed, is_approximate = determine_read_date(date_read_str, shelves)
            
            # Skip books that are clearly not read (to-read, currently-reading)
            exclusive_shelf = row.get('Exclusive Shelf', '').lower()
            if exclusive_shelf in ['to-read', 'currently-reading']:
                skipped_count += 1
                continue
            
            # Extract other data
            rating = row.get('My Rating', '').strip()
            rating_int = int(rating) if rating and rating != '0' else None
            
            genre = determine_genre(shelves, title, author)
            review = clean_review_text(row.get('My Review', ''))
            
            # Create filename
            filename = clean_filename(title) + '.md'
            file_path = output_path / filename
            
            # Create markdown content
            frontmatter = f"""---
title: "{title}"
author: "{author}"
genre: "{genre}"
dateCompleted: {date_completed}"""
            
            if rating_int:
                frontmatter += f"\nrating: {rating_int}"
            
            frontmatter += "\n---\n\n"
            
            # Add note for approximate dates
            content = frontmatter
            if is_approximate:
                content += f"*Read sometime in {date_completed[:4]}*\n\n"
                approximate_count += 1
            elif date_completed == "Unknown":
                content += "*Read date unknown*\n\n"
                unknown_count += 1
            
            content += (review if review else "")
            
            # Write file
            with open(file_path, 'w', encoding='utf-8') as mdfile:
                mdfile.write(content)
            
            print(f"Created: {filename}" + 
                  (" (approximate date)" if is_approximate else "") +
                  (" (unknown date)" if date_completed == "Unknown" else ""))
            converted_count += 1
    
    print("\nConversion complete!")
    print(f"Converted: {converted_count} books")
    print(f"  - Exact dates: {converted_count - approximate_count - unknown_count}")
    print(f"  - Approximate dates: {approximate_count}")
    print(f"  - Unknown dates: {unknown_count}")
    print(f"Skipped: {skipped_count} books (to-read/currently-reading)")


def main():
    if len(sys.argv) != 2:
        print("Usage: python convert_goodreads_csv.py <path_to_goodreads_csv>")
        print("Example: python scripts/convert_goodreads_csv.py src/data/books/goodreads_library_export.csv")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    
    if not os.path.exists(csv_file):
        print(f"Error: CSV file '{csv_file}' not found")
        sys.exit(1)
    
    # Output to the books content directory
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    output_dir = project_root / "src" / "content" / "books"
    
    print(f"Converting {csv_file} to markdown files in {output_dir}")
    convert_csv_to_markdown(csv_file, output_dir)


if __name__ == "__main__":
    main()