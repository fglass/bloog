import feedparser
from config import DATA_DIR
from newspaper import Article

RSS_FEEDS = [
    "https://doordash.engineering/feed",
]


def download_feed(url: str):
    feed = feedparser.parse(url)
    print(f"Found {len(feed.entries)} entries in {url}")

    for entry in feed.entries:
        download_article(entry["link"])


def download_article(url: str):
    title, text = load_article(url)
    filepath = f"{DATA_DIR}/{title}.txt"

    with open(filepath, "w") as f:
        f.write(text)

    print(f"✅ {title}")


def load_article(url) -> tuple[str, str]:
    article = Article(url)

    article.download()
    article.parse()

    return article.title, article.text


if __name__ == "__main__":
    # https://blog.feedspot.com/engineering_rss_feeds/
    # https://backfeed.app
    feed_url = "https://doordash.engineering/feed"
    download_feed(feed_url)

    # article_url = "https://doordash.engineering/2021/07/14/open-source-search-indexing"
    # download_article(article_url)
