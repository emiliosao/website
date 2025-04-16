import feedparser
import os
from datetime import datetime
import re

# Letterboxd RSS feed URL
rss_url = "https://letterboxd.com/emiliosao/rss/"

# Directory for blog posts
blog_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../content/blog/letterboxd/")

# Fetch the RSS feed
feed = feedparser.parse(rss_url)

# Get the most recent entries from the RSS feed
if feed.entries:
    # Track existing blog files
    existing_files = {f for f in os.listdir(blog_dir) if f.endswith(".md")}

    for entry in feed.entries:
        try:
            # Use letterboxd:watchedDate with correct date format
            watched_date = datetime.strptime(entry.get('letterboxd_watcheddate', ''), "%Y-%m-%d")
        except Exception as e:
            print(f"Error parsing date for entry {entry.title}: {e}")
            continue

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
        date = watched_date.strftime("%Y-%m-%d")

        # Extract poster from the description
        poster_match = re.search(r'<img src="([^"]+)"', entry.summary or '')
        poster_url = poster_match.group(1) if poster_match else ''

        # Set the description to just the rating or rewatch symbol
        if rating:
            description = rating
            summary = f"{rating} on Letterboxd"
        elif rewatch:
            description = rewatch
            summary = f"{rewatch} on Letterboxd"
        else:
            description = "Logged"
            summary = "Logged on Letterboxd"

        # Filename format using watched_date
        date_part = watched_date.strftime("%y%m%d")
        clean_title = re.sub(r"[^\w\s-]", "", title).replace(" ", "_")
        filename = f"{date_part}-{clean_title}.md"
        filepath = os.path.join(blog_dir, filename)

        # Skip if already exists
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
                # Add the cover information
                if poster_url:
                    f.write(f"cover:\n    image: \"{poster_url}\"\n    alt: \"{title} movie poster\"\n")
                # Add the description with just the rating or rewatch symbol
                f.write(f"description: \"{description}\"\n")
                f.write("---\n")

                # Standard "Logged on Letterboxd" header with link
                f.write(f"## [Logged on Letterboxd]({entry.link})\n\n")

            print(f"Successfully added: {title}")
        except Exception as e:
            print(f"Error while writing file {filename}: {e}")
else:
    print("No new entries found.")
