import os
import pysolr
from config import DATA_DIR, SOLR_URL


def index():
    solr = pysolr.Solr(SOLR_URL, always_commit=True, timeout=10)
    solr.ping()

    documents = []

    for filename in os.listdir(DATA_DIR):
        with open(f"{DATA_DIR}/{filename}", "r") as f:
            title = filename[:-4]
            text = f.read()
            documents.append(
                {
                    "id": title,
                    "title_txt_en_split": title,
                    "content_txt_en_split": text,
                }
            )

    solr.add(documents)
    print(f"✅ Indexed {len(documents)} documents")


if __name__ == "__main__":
    # https://solr.apache.org/guide/solr/latest/deployment-guide/solr-in-docker.html
    # docker run -d -v "$PWD/solrdata:/var/solr" -p 8983:8983 --name my_solr solr solr-precreate articles
    index()
