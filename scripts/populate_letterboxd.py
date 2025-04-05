import feedparser
import os
from datetime import datetime
import re
import xml.etree.ElementTree as ET

# Letterboxd RSS feed URL
rss_url = "https://letterboxd.com/emiliosao/rss/"

# Directory for blog posts
blog_dir = "content/blog/"

# Ensure the blog directory exists
os.makedirs(blog_dir, exist_ok=True)

# Fetch the RSS feed
feed = feedparser.parse(rss_url)

# Target year for initial population
target_year = 2025

for entry in feed.entries:
    try:
        # Use the pubDate to parse the date
        entry_date = datetime(*entry.published_parsed[:6])
    except Exception as e:
        print(f"Error parsing date for entry {entry.title}: {e}")
        continue

    if entry_date.year != target_year:
        print(f"Skipped (not from {target_year}): {entry.title} ({entry_date.year})")
        continue

    print(f"Processing: {entry.title}")

    # Extract rating from the title - includes half-star symbol ½
    rating_match = re.search(r'★+½?', entry.title)
    rating = rating_match.group(0) if rating_match else ''

    # Check rewatch status
    rewatch = ''
    # Check if the rewatch tag exists in the raw XML
    if hasattr(entry, 'tags'):
        for tag in entry.tags:
            if tag.get('term', '').lower() == 'rewatch':
                rewatch = '🔄'
                break

    # Fallback to checking rewatch status via attributes or title
    if not rewatch:
        # Check the letterboxd:rewatch element
        rewatch_elem = entry.get('letterboxd_rewatch', '')
        if rewatch_elem and rewatch_elem.lower() == 'yes':
            rewatch = '🔄'

    # Additional fallback - check title for rewatch-related keywords
    if not rewatch:
        rewatch_keywords = ['rewatch', 're-watch', 'rewatched']
        if any(keyword in entry.title.lower() for keyword in rewatch_keywords):
            rewatch = '🔄'

    # Remove rating from the title
    title = re.sub(r' - ★+½?|:|/|\"', '', entry.title).strip()
    date = entry_date.strftime("%Y-%m-%d")

    # Extract poster and watched date from the description
    poster_match = re.search(r'<img src="([^"]+)"', entry.summary or '')
    poster_url = poster_match.group(1) if poster_match else ''

    # Construct the summary based on the rating and rewatch status
    if rating:
        summary = f"{rating} on Letterboxd"
    elif rewatch:
        summary = f"🔄 on Letterboxd"
    else:
        summary = "Logged on Letterboxd"

    # Filename format
    date_part = entry_date.strftime("%y%m%d")
    clean_title = re.sub(r"[^\w\s-]", "", title).replace(" ", "_")
    filename = f"{date_part}-{clean_title}.md"
    filepath = os.path.join(blog_dir, filename)

    if os.path.exists(filepath):
        print(f"Already exists: {title}")
        continue

    try:
        with open(filepath, "w") as f:
            print(f"Writing to file: {filepath}")
            f.write(f"---\ntitle: \"{title}\"\ndate: {date}\ntags: ['letterboxd']\n")
            f.write(f"source: 'Letterboxd'\n")
            f.write(f"link: \"{entry.link}\"\n")
            f.write(f"summary: \"{summary}\"\n")
            f.write("---\n\n")

            # Write the rating as a clickable header link (with rewatch if present)
            f.write(f"## [{summary}]({entry.link})\n\n")

            # Add poster and watched date information
            if poster_url:
                f.write(f"<p><img src=\"{poster_url}\" /></p>\n")

            # Add watched date from the description
            watched_date_match = re.search(r'Watched on ([^<]+)', entry.summary or '')
            if watched_date_match:
                f.write(f"<p>{watched_date_match.group(0)}</p>")

        print(f"Successfully added: {title}")
    except Exception as e:
        print(f"Error while writing file {filename}: {e}")

print("Initial population of blog posts completed!")