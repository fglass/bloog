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
            metadata = _parse_frontmatter(f)
            content = f.read()
            documents.append(_to_document_model(filename, metadata, content))

    solr.add(documents)
    print(f"✅ Added {len(documents)} documents")


def _parse_frontmatter(f: TextIOWrapper) -> dict:
    metadata = {}

    for line in f.readlines():
        if line == "---\n":
            break
        else:
            split_idx = line.find(":")
            key, value = line[:split_idx], line[split_idx + 2 :]
            metadata[key] = "".join(value).strip()

    return metadata


def _to_document_model(filename: str, metadata: dict, content: str) -> dict:
    source = filename.split("::")[0]
    return {
        "id": filename,
        "content_txt_en_split": content,
        "title_txt_en_split": metadata.get("title"),
        "summary_txt_en_split": metadata.get("summary"),
        "created_at_dt": metadata.get("created"),
        "url_s": metadata.get("url"),
        "author_s": metadata.get("author"),
        "source_s": source,
    }


if __name__ == "__main__":
    index(drop=True)
