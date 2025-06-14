from pathlib import Path
import feedparser
import requests
from bs4 import BeautifulSoup
import textwrap

FEED_URL = "https://spacetales.in/feed/"
README_PATH = Path("README.md")
MAX_ITEMS = 6


def extract_image(content):
    soup = BeautifulSoup(content, "html.parser")
    img = soup.find("img")
    return img["src"] if img else "https://via.placeholder.com/250x140.png?text=No+Image"


def generate_blog_cards():
    feed = feedparser.parse(FEED_URL)
    entries = feed.entries[:MAX_ITEMS]

    blog_cards = '<table><tr>'
    count = 0

    for entry in entries:
        title = entry.title
        link = entry.link
        pub_date = entry.published.split(',')[-1].strip()
        content = entry.get("content", [{}])[0].get("value", "")
        image_url = extract_image(content)

        card_html = (
            '<td align="center" width="33%" style="padding: 10px;">'
            f'<a href="{link}" target="_blank">'
            f'<img src="{image_url}" alt="{title}" width="250" height="140" style="border-radius:10px;"><br>'
            f'<b>{title}</b>'
            '</a><br>'
            # f'<sub>📅 {pub_date}</sub>'
            '</td>'
        )

        blog_cards += card_html
        count += 1

        if count % 3 == 0 and count != MAX_ITEMS:
            blog_cards += "</tr>\n<tr>"

    if count % 3 != 0:
        blog_cards += "</tr>"

    blog_cards += "</table>"
    return blog_cards


def update_readme(blog_cards):
    if README_PATH.exists():
        content = README_PATH.read_text(encoding="utf-8")
    else:
        content = ""

    start_tag = "<!-- BLOG-CARDS:START -->"
    end_tag = "<!-- BLOG-CARDS:END -->"

    new_section = f"{start_tag}\n{blog_cards}\n{end_tag}"

    if start_tag in content and end_tag in content:
        updated_content = content.split(start_tag)[0] + new_section + content.split(end_tag)[1]
    else:
        updated_content = content + f"\n\n{new_section}"

    README_PATH.write_text(updated_content, encoding="utf-8")
    print("✅ Blog cards section updated in README.md")


if __name__ == "__main__":
    cards = generate_blog_cards()
    update_readme(cards)

