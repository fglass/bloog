import os
import feedparser
from config import DATA_DIR
from newspaper import Article


# https://backfeed.app
# https://blog.feedspot.com/engineering_rss_feeds/
BACKFILLED_RSS_FEEDS = [
    "https://backfeed.app/eOL3r1ethXnHeNqBEy/https://doordash.engineering/feed"
]


def download_feed(feed_url: str):
    print(feed_url)

    feed = feedparser.parse(feed_url)
    print(f"\tFound {len(feed.entries)} entries in feed")

    n_new = 0

    for entry in feed.entries:
        article_url = entry["link"]
        is_new = download_article(article_url)
        n_new += 1 if is_new else 0

    print(f"\tDownloaded {n_new} new articles")


def download_article(url: str) -> bool:
    title, content = load_article(url)

    if not title or not content:
        return False

    filepath = f"{DATA_DIR}/{title}.txt"

    if os.path.exists(filepath):
        return False

    with open(filepath, "w") as f:
        f.write(content)

    print(f"\t✅ {title}")
    return True


def load_article(url) -> tuple[str, str]:
    article = Article(url)

    article.download()
    article.parse()

    return article.title, article.text


if __name__ == "__main__":
    for feed_url in BACKFILLED_RSS_FEEDS:
        download_feed(feed_url)
