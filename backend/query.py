import pysolr
from config import SOLR_URL


def search(query: str) -> list[str]:
    if query == "":
        return []

    results = _search_solr(query)

    if results.debug:
        print(results.debug)

    return [_to_view_model(doc) for doc in results]


def _search_solr(raw_query: str) -> pysolr.Results:
    solr = pysolr.Solr(SOLR_URL, always_commit=True)
    query = f"title_txt_en_split:{raw_query} OR content_txt_en_split:{raw_query}"
    return solr.search(query, debug=False)


def _to_view_model(doc: dict) -> dict:
    return {
        "id": doc.get("id"),
        "title": doc.get("title_txt_en_split"),
        "createdAt": doc.get("created_at_dt"),
        "url": doc.get("url_s"),
        "source": doc.get("source_s"),
        "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
    }


if __name__ == "__main__":
    for doc in search(query="code"):
        print(f"\t- {doc}")
