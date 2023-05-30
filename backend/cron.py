from article import download_feed
from index import index


RSS_FEEDS = ["https://doordash.engineering/feed"]


def cron():
    print("Downloading feeds...")
    for feed_url in RSS_FEEDS:
        download_feed(feed_url)

    print("Adding articles to index...")
    index()


if __name__ == "__main__":
    cron()
