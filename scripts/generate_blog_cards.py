import feedparser
from datetime import datetime
import re

RSS_FEED_URL = "https://spacetales.in/feed/"
MAX_POSTS = 6
README_PATH = "README.md"
START_TAG = "<!-- BLOG-CARDS:START -->"
END_TAG = "<!-- BLOG-CARDS:END -->"

import re

import requests
from bs4 import BeautifulSoup

def extract_image(entry):
    # Try fetching Open Graph image from the actual blog URL
    try:
        url = entry.get("link", "")
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")
        og_image = soup.find("meta", property="og:image")
        if og_image and og_image.get("content"):
            return og_image["content"]
    except Exception as e:
        print(f"Failed to get image for {entry.get('title', '')}: {e}")
    
    return None



def get_blog_posts():
    feed = feedparser.parse(RSS_FEED_URL)
    posts = []
    for entry in feed.entries[:MAX_POSTS]:
        title = entry.title
        link = entry.link
        date = datetime(*entry.published_parsed[:6]).strftime("%b %d, %Y")
        image = extract_image(entry)
        posts.append((title, link, date, image))
    return posts


def format_as_markdown(posts):
    markdown = ""
    for title, link, date, image in posts:
        if image:
            markdown += (
                f'<p align="center">\n'
                f'  <a href="{link}" target="_blank">\n'
                f'    <img src="{image}" width="300" alt="{title}"/><br/>\n'
                f'    <b>{title}</b>\n'
                f'  </a><br/>\n'
                f'  <sub>📅 {date}</sub>\n'
                f'</p>\n\n'
            )
        else:
            markdown += (
                f'<p align="center">\n'
                f'  <a href="{link}" target="_blank">\n'
                f'    <b>{title}</b>\n'
                f'  </a><br/>\n'
                f'  <sub>📅 {date}</sub>\n'
                f'</p>\n\n'
            )
    return markdown.strip()





def update_readme(posts_md):
    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    start = content.find(START_TAG) + len(START_TAG)
    end = content.find(END_TAG)

    new_content = content[:start] + "\n" + posts_md + "\n" + content[end:]

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)

if __name__ == "__main__":
    posts = get_blog_posts()
    posts_md = format_as_markdown(posts)
    update_readme(posts_md)

