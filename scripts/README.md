# Goodreads CSV Converter

This script converts a Goodreads library export CSV into markdown files for the Astro books content collection.

## Usage

1. Export your Goodreads library:
   - Go to Goodreads.com → My Books → Import and Export
   - Click "Export Library" 
   - Save the CSV file to `src/data/books/goodreads_library_export.csv`

2. Run the conversion script:
   ```bash
   python scripts/convert_goodreads_csv.py src/data/books/goodreads_library_export.csv
   ```

3. The script will create individual `.md` files in `src/content/books/` for each book you've read.

## What it does

- **Filters read books**: Only processes books with a "Date Read" 
- **Extracts metadata**: Title, author, rating, completion date
- **Determines genre**: Uses Goodreads shelves to categorize books
- **Cleans reviews**: Removes HTML and formats review text
- **Creates filenames**: Converts titles to clean, URL-safe filenames

## Output format

Each book becomes a markdown file like:

```markdown
---
title: "Book Title"
author: "Author Name"
genre: "Fiction"
dateCompleted: 2024-03-15
rating: 4
---

Your review text here (if any)...
```

## Genre mapping

The script maps common Goodreads shelf names to genres:
- `non-fiction` → Non-fiction
- `fantasy` → Fantasy  
- `sci-fi` → Science Fiction
- `biography` → Biography
- `philosophy` → Philosophy
- And many more...

Books without clear genre indicators default to "Fiction".