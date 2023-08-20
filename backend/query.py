import html
import pysolr
import re
from config import SOLR_URL

PAGE_SIZE = 9
MAX_DESCRIPTION_LENGTH = 140


def search(query: str, sort_option: str, page_number: int, debug: bool = False) -> dict:
    if query == "":
        return []

    results = _search_solr(query, sort_option, page_number, debug)

    if results.debug:
        print(results.debug)

    return {"total": results.hits, "results": [_to_view_model(doc) for doc in results]}


def _search_solr(
    raw_query: str, sort_option: str, page_number: int, debug: bool
) -> pysolr.Results:
    query = _to_solr_query(raw_query)
    params = {"rows": PAGE_SIZE, "start": page_number * PAGE_SIZE, "debug": debug}

    if sort_option == "newest":
        params["sort"] = "created_at_dt desc"

    solr = pysolr.Solr(SOLR_URL, always_commit=True)
    return solr.search(query, **params)


def _to_solr_query(raw_query: str) -> str:
    return f"title_txt_en_split:{raw_query} OR title_txt_en_split:{raw_query}* OR content_txt_en_split:{raw_query}"


def _to_view_model(doc: dict) -> dict:
    description = doc.get("summary_txt_en_split", "")
    sanitised_description = re.sub("<[^<]+?>", "", html.unescape(description))
    return {
        "id": doc.get("id"),
        "title": doc.get("title_txt_en_split"),
        "createdAt": doc.get("created_at_dt"),
        "url": doc.get("url_s"),
        "source": doc.get("source_s"),
        "description": sanitised_description[:MAX_DESCRIPTION_LENGTH],
    }


if __name__ == "__main__":
    for doc in search(query="code"):
        print(f"\t- {doc}")
