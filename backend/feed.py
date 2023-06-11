import feedparser
import os
from datetime import datetime
from config import DATA_DIR
from newspaper import Article


# https://backfeed.app
# https://blog.feedspot.com/engineering_rss_feeds/
VERSION = 1
BACKFILLED_RSS_FEEDS = {
    "DoorDash": "https://backfeed.app/eOL3r1ethXnHeNqBEy/https://doordash.engineering/feed"
}


def download_feed(feed_key: str, feed_url: str):
    print(f"{feed_key}: {feed_url}")

    feed = feedparser.parse(feed_url)
    print(f"\tFound {len(feed.entries)} entries in feed")

    n_new = 0

    for entry in feed.entries:
        article_url = entry.get("link")
        tags = [tag.get("term") for tag in entry.get("tags", [])]
        created_at_raw = entry.get("published_parsed")
        created_at_dt = datetime.now()

        if created_at_raw is not None:
            created_at_dt = datetime(*created_at_raw[:6])

        article_metadata = {
            "title": entry.get("title"),
            "created": created_at_dt.isoformat(),
            "author": entry.get("author"),
            "tags": ",".join(tags),
            "url": article_url,
        }

        is_new = _download_article(feed_key, article_url, article_metadata)
        n_new += 1 if is_new else 0

    print(f"\tDownloaded {n_new} new articles")


def _download_article(feed: str, url: str | None, metadata: dict) -> bool:
    if not url:
        return False

    title = metadata.get("title")
    content = _load_article(url)

    if not title or not content:
        return False

    filepath = f"{DATA_DIR}/{feed}::{title}.txt"

    if os.path.exists(filepath):  # TODO: compare version
        return False

    frontmatter = _create_frontmatter(metadata)

    with open(filepath, "w") as f:
        f.write(frontmatter)
        f.write(content)

    print(f"\t✅ {title}")
    return True


def _load_article(url) -> str:
    article = Article(url)

    article.download()
    article.parse()

    return article.text


def _create_frontmatter(metadata: dict) -> str:
    frontmatter = [f"version: {VERSION}"]

    for k, v in metadata.items():
        frontmatter.append(f"{k}: {v}")

    frontmatter.append("---\n")

    return "\n".join(frontmatter)


if __name__ == "__main__":
    for feed_key, feed_url in BACKFILLED_RSS_FEEDS.items():
        download_feed(feed_key, feed_url)
