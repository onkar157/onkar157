import feedparser
from pathlib import Path

FEED_URL = "https://spacetales.in/feed/"
README_PATH = Path("README.md")
MAX_ITEMS = 6

def generate_blog_cards():
    feed = feedparser.parse(FEED_URL)
    blog_cards = "<table><tr>"
    count = 0

    for entry in feed.entries[:MAX_ITEMS]:
        title = entry.title
        link = entry.link
        image_url = ""

        if "media_content" in entry:
            image_url = entry.media_content[0]["url"]
        elif "media_thumbnail" in entry:
            image_url = entry.media_thumbnail[0]["url"]
        elif "content" in entry:
            import re
            match = re.search(r'<img[^>]+src="([^">]+)"', entry.content[0].value)
            if match:
                image_url = match.group(1)

        card_html = f'''
        <td align="center" width="50%" style="padding: 10px;">
            <a href="{link}" target="_blank">
                <img src="{image_url}" alt="{title}" width="250" height="140" style="border-radius:10px;"><br>
                <b>{title}</b>
            </a>
        </td>'''
        blog_cards += card_html
        count += 1

        if count % 2 == 0 and count != MAX_ITEMS:
            blog_cards += "</tr>\n<tr>"

    if count % 2 != 0:
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

    new_section = f"{start_tag}\n<!-- prettier-ignore-start -->\n{blog_cards}\n<!-- prettier-ignore-end -->\n{end_tag}"

    if start_tag in content and end_tag in content:
        updated_content = content.split(start_tag)[0] + new_section + content.split(end_tag)[1]
    else:
        updated_content = content + f"\n\n{new_section}"

    README_PATH.write_text(updated_content, encoding="utf-8")
    print("✅ Blog cards section updated in README.md")

if __name__ == "__main__":
    cards = generate_blog_cards()
    update_readme(cards)
