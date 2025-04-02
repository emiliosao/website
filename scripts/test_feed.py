import feedparser

rss_url = "https://letterboxd.com/emiliosao/rss/"
feed = feedparser.parse(rss_url)

print(f"Feed Title: {feed.feed.title}")
print(f"Number of Entries: {len(feed.entries)}")
for entry in feed.entries[:5]:  # Print the first 5 entries for verification
    print(f"Title: {entry.title}")
    print(f"Link: {entry.link}")
    print(f"Published: {entry.published}")
    print("-" * 50)
