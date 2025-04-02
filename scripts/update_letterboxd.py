import feedparser
import os
from datetime import datetime
import re

# Letterboxd RSS feed URL
rss_url = "https://letterboxd.com/emiliosao/rss/"

# Directory for blog posts
blog_dir = "/var/www/website/content/blog/"

# Fetch the RSS feed
feed = feedparser.parse(rss_url)

# Get the most recent entry from the RSS feed
if feed.entries:
    # Track existing blog files
    existing_files = {f for f in os.listdir(blog_dir) if f.endswith(".md")}

    for entry in feed.entries:
        try:
            entry_date = datetime(*entry.published_parsed[:6])
        except Exception as e:
            print(f"Error parsing date for entry {entry.title}: {e}")
            continue

        # Extract rating, liked, and rewatch from the title
        rating_match = re.search(r'★+', entry.title)
        rating = rating_match.group(0) if rating_match else ''

        # Extract rewatch information from the RSS entry
        rewatch = '🔄' if entry.get('letterboxd:rewatch', '').lower() == 'yes' else ''

        # Extract liked information from the content
        liked = '🧡' if 'liked' in entry.summary.lower() else ''

        title = re.sub(r' - ★+½?|:|/|"', '', entry.title).strip()
        date = entry_date.strftime("%Y-%m-%d")
        content = entry.summary.strip() if entry.summary else ""
        url = entry.link

        # Construct the summary based on the rating
        if rating:
            summary = f"{rating} on Letterboxd"
        else:
            summary = "Logged on Letterboxd"

        # Filename format
        date_part = entry_date.strftime("%y%m%d")
        clean_title = re.sub(r"[^\w\s-]", "", title).replace(" ", "_")
        filename = f"{date_part}-{clean_title}.md"
        filepath = os.path.join(blog_dir, filename)

        # Check if the file already exists
        if os.path.exists(filepath):
            print(f"Already exists: {title}")
            continue

        try:
            with open(filepath, "w") as f:
                print(f"Writing to file: {filepath}")
                f.write(f"---\ntitle: \"{title}\"\ndate: {date}\ntags: ['letterboxd']\n")
                f.write(f"source: 'Letterboxd'\n")
                f.write(f"link: \"{url}\"\n")
                f.write(f"summary: \"{summary}\"\n")
                f.write("---\n\n")
                # Write the rating as a clickable header link
                f.write(f"## [{rating}]({url}) {liked} {rewatch}\n\n")
                f.write(content)
            print(f"Successfully added: {title}")
        except Exception as e:
            print(f"Error while writing file {filename}: {e}")
else:
    print("No new entries found.")
