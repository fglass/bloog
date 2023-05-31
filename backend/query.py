import pysolr
from config import SOLR_URL


def search(query: str) -> list[str]:
    results = _search_solr(query)

    if results.debug:
        print(results.debug)

    return [doc.get("id") for doc in results]


def _search_solr(raw_query: str) -> pysolr.Results:
    solr = pysolr.Solr(SOLR_URL, always_commit=True)
    query = f"title_txt_en_split:{raw_query} OR content_txt_en_split:{raw_query}"
    return solr.search(query, debug=False)


if __name__ == "__main__":
    for doc in search(query="code"):
        print(f"\t- {doc}")
