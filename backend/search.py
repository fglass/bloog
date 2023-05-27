import pysolr
from config import SOLR_URL


def search():
    solr = pysolr.Solr(SOLR_URL, always_commit=True)
    results = solr.search("*:*")
    print(f"Found {len(results)} results")

    for result in results:
        result.pop("content_txt")
        print(result)

if __name__ == "__main__":
    search()