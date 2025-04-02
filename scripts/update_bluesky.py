import os
from datetime import datetime
from atproto import Client

# Your Bluesky credentials from environment variables
USERNAME = os.environ.get("BLUESKY_USERNAME", "")
PASSWORD = os.environ.get("BLUESKY_PASSWORD", "")

# Check if credentials are available
if not USERNAME or not PASSWORD:
    print("Error: Bluesky credentials not found in environment variables")
    print("Please set BLUESKY_USERNAME and BLUESKY_PASSWORD environment variables")
    exit(1)

# Directory for blog posts
blog_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../content/blog/")

# Initialize the Bluesky client
client = Client()
client.login(USERNAME, PASSWORD)

# Get the latest post from your profile
feed = client.get_feed("emiliosao.me")
latest_post = feed['feed'][0]

# Extract post details
post_id = latest_post['uri'].split("/")[-1]
post_text = latest_post['post']['text']
post_date = datetime.strptime(latest_post['post']['createdAt'], "%Y-%m-%dT%H:%M:%S.%fZ")
post_url = f"https://bsky.app/profile/emiliosao.me/post/{post_id}"

# Create a clean and formatted filename
date_part = post_date.strftime("%y%m%d")
clean_title = post_text[:50].replace(" ", "_").replace("/", "_")
filename = f"{date_part}-bluesky_{clean_title}.md"
filepath = os.path.join(blog_dir, filename)

# Check if the file already exists
if os.path.exists(filepath):
    print(f"Already exists: {filename}")
else:
    try:
        with open(filepath, "w") as f:
            print(f"Writing to file: {filepath}")
            f.write(f"---\ntitle: \"Bluesky Post\"\ndate: {post_date.strftime('%Y-%m-%d')}\ntags: ['bluesky']\n")
            f.write(f"source: 'Bluesky'\n")
            f.write(f"link: \"{post_url}\"\n")
            f.write("---\n\n")
            f.write(f"{{{{< bluesky \"{post_url}\" >}}}}\n")
            f.write(f"\n{post_text}\n")
        print(f"Successfully added: {filename}")
    except Exception as e:
        print(f"Error while writing file {filename}: {e}")
