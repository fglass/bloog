import html
import pysolr
import re
from config import SOLR_URL

PAGE_SIZE = 9
MAX_DESCRIPTION_LENGTH = 140


def search(query: str, sort_option: str, page_number: int, debug: bool = False) -> dict:
    if query == "":
        return {"total": 0, "results": []}

    results = _query_solr(query, sort_option, page_number, debug)

    if results.debug:
        print(results.debug)

    return {"total": results.hits, "results": [_to_view_model(doc) for doc in results]}


def _query_solr(  # TODO: async
    query_string: str, sort_option: str, page_number: int, debug: bool
) -> pysolr.Results:
    query = _to_solr_query(sort_option, page_number, debug)
    solr = pysolr.Solr(SOLR_URL, always_commit=True)
    return solr.search(query_string, **query)


def _to_solr_query(sort_option: str, page_number: int, debug: bool) -> dict:
    query = {
        "defType": "edismax",
        "qf": "title_txt_en_split_edge_ngram^5 content_txt_en_split",
        "rows": PAGE_SIZE,
        "start": page_number * PAGE_SIZE,
        "sort": "score desc",
        "debug": debug,
    }

    if sort_option == "newest":
        query["sort"] = "created_at_dt desc"

    query["sort"] += ", id desc"  # Stable sort for pagination

    return query


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
    for doc in search(query="code", sort_option="newest", page_number=0, debug=True)[
        "results"
    ]:
        print(f"\t- {doc}")
