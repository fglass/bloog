from feed import download_feed
from index import index


RSS_FEEDS = {
    "DoorDash": "https://doordash.engineering/feed",
}


def cron():
    print("Downloading feeds...")
    for feed_key, feed_url in RSS_FEEDS.items():
        download_feed(feed_key, feed_url)

    print("Adding articles to index...")
    index()


if __name__ == "__main__":
    cron()
