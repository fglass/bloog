from config import DATA_DIR
from newspaper import Article


def download(url: str):
    title, text = load_article(url)
    filepath = f"{DATA_DIR}/{title}.txt"

    with open(filepath, "w") as f:
        f.write(text)

    print(f"✅ {title}")


def load_article(url) -> tuple[str, str]:
    article = Article(url)
    
    article.download()
    article.parse()
    
    return article.title, article.text


if __name__ == "__main__":
    article_url = "https://doordash.engineering/2021/07/14/open-source-search-indexing"
    download(article_url)
