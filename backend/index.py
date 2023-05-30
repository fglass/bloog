import os
import pysolr
from config import DATA_DIR, SOLR_URL


def index(drop: bool = False):
    solr = pysolr.Solr(SOLR_URL, timeout=10, always_commit=True)
    solr.ping()

    if drop:
        solr.delete(q="*:*")

    documents = []

    for filename in os.listdir(DATA_DIR):
        with open(f"{DATA_DIR}/{filename}", "r") as f:
            title = filename.removesuffix(".txt")
            content = f.read()
            documents.append(
                {
                    "id": title,
                    "title_txt_en_split": title,
                    "content_txt_en_split": content,
                }
            )

    solr.add(documents)
    print(f"✅ Added {len(documents)} documents")


if __name__ == "__main__":
    # https://solr.apache.org/guide/solr/latest/deployment-guide/solr-in-docker.html
    # docker run -d -v "$PWD/solrdata:/var/solr" -p 8983:8983 --name my_solr solr solr-precreate articles
    index()
