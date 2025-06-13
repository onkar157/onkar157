import feedparser
from datetime import datetime

RSS_FEED_URL = "https://spacetales.in/feed/"
MAX_POSTS = 6
README_PATH = "README.md"
START_TAG = "<!-- BLOG-CARDS:START -->"
END_TAG = "<!-- BLOG-CARDS:END -->"

def get_blog_posts():
    feed = feedparser.parse(RSS_FEED_URL)
    posts = []
    for entry in feed.entries[:MAX_POSTS]:
        title = entry.title
        link = entry.link
        date = datetime(*entry.published_parsed[:6]).strftime("%b %d, %Y")
        posts.append((title, link, date))
    return posts

def format_as_html_table(posts):
    html = "<table><tr>\n"
    for i, (title, link, date) in enumerate(posts):
        html += f"""<td align="center" width="33%">
  <a href="{link}" target="_blank">
    <b>{title}</b><br/>
    <sub>{date}</sub>
  </a>
</td>\n"""
        if (i + 1) % 3 == 0 and i != len(posts) - 1:
            html += "</tr><tr>\n"
    html += "</tr></table>"
    return html

def update_readme(posts_html):
    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    start = content.find(START_TAG) + len(START_TAG)
    end = content.find(END_TAG)

    new_content = content[:start] + "\n" + posts_html + "\n" + content[end:]

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)

if __name__ == "__main__":
    posts = get_blog_posts()
    posts_html = format_as_html_table(posts)
    update_readme(posts_html)
