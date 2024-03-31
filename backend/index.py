import os
import pysolr
from config import DATA_DIR, SOLR_URL
from io import TextIOWrapper


def index(drop: bool = False):
    solr = pysolr.Solr(SOLR_URL, timeout=10, always_commit=True)
    solr.ping()

    if drop:
        solr.delete(q="*:*")

    documents = []

    for filename in os.listdir(DATA_DIR):
        with open(f"{DATA_DIR}/{filename}", "r") as f:
            metadata, content = _parse_file(f.readlines())
            documents.append(_to_document_model(filename, metadata, content))

    solr.add(documents)
    print(f"✅ Indexed {len(documents)} documents")


def _parse_file(lines: list[str]) -> tuple[dict, str]:
    metadata = {}
    content = []

    for idx, line in enumerate(lines):
        if line == "---\n":
            content = lines[idx + 1 :]
            break

        split_idx = line.find(":")
        key, value = line[:split_idx], line[split_idx + 2 :]
        metadata[key] = "".join(value).strip()

    content = " ".join(content).replace("\n", " ")

    return metadata, content


def _to_document_model(filename: str, metadata: dict, content: str) -> dict:
    source = filename.split("::")[0]
    return {
        "id": filename,
        "content_txt_en_split": content,
        "title_txt_en_split": metadata.get("title"),
        # Custom edge n-gram field type
        "title_txt_en_split_edge_ngram": metadata.get("title"),
        "summary_txt_en_split": metadata.get("summary"),
        "created_at_dt": metadata.get("created"),
        "url_s": metadata.get("url"),
        "author_s": metadata.get("author"),
        "source_s": source,
    }


if __name__ == "__main__":
    index(drop=True)
