import pysolr
from config import SOLR_URL


def search(query: str):
    results = _search_solr(query)
    print(f"🔍 Found {len(results)} results:")

    for doc in results:
        print(f"\t- {doc.get('id')}")

    if results.debug:
        print(results.debug)


def _search_solr(raw_query: str) -> pysolr.Results:
    solr = pysolr.Solr(SOLR_URL, always_commit=True)
    query = f"title_txt_en_split:{raw_query} OR content_txt_en_split:{raw_query}"
    return solr.search(query, debug=False)


if __name__ == "__main__":
    search(query="code")
