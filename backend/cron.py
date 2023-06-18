from config import RSS_FEEDS
from feed import download_feed
from index import index


RECENT_FEEDS = {k: v.split("qBEy/")[1] for k, v in RSS_FEEDS.items()}


def cron():
    print("Downloading feeds...")
    for feed_key, feed_url in RECENT_FEEDS.items():
        download_feed(feed_key, feed_url)

    print("Adding articles to index...")
    index()


if __name__ == "__main__":
    cron()
