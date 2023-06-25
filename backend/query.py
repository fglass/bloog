import html
import pysolr
from config import SOLR_URL

PAGE_SIZE = 9


def search(query: str, sort_option: str, page_number: int) -> dict:
    if query == "":
        return []

    results = _search_solr(query, sort_option, page_number)

    if results.debug:
        print(results.debug)

    return {"total": results.hits, "results": [_to_view_model(doc) for doc in results]}


def _search_solr(raw_query: str, sort_option: str, page_number: int) -> pysolr.Results:
    solr = pysolr.Solr(SOLR_URL, always_commit=True)
    query = f"title_txt_en_split:{raw_query} OR content_txt_en_split:{raw_query}"
    params = {"rows": PAGE_SIZE, "start": page_number * PAGE_SIZE, "debug": False}

    if sort_option == "newest":
        params["sort"] = "created_at_dt desc"

    return solr.search(query, **params)


def _to_view_model(doc: dict) -> dict:
    return {
        "id": doc.get("id"),
        "title": doc.get("title_txt_en_split"),
        "createdAt": doc.get("created_at_dt"),
        "url": doc.get("url_s"),
        "source": doc.get("source_s"),
        "description": html.unescape(
            doc.get("summary_txt_en_split", "")
            .replace("<p>", "")
            .replace("</p>", "")[:140]
        ),
    }


if __name__ == "__main__":
    for doc in search(query="code"):
        print(f"\t- {doc}")
