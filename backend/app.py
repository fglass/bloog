import query
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# uvicorn app:app --reload
# docker run -d -v "$PWD/solrdata:/var/solr" -p 8983:8983 --name my_solr solr solr-precreate articles
app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/search")
def search(q: str, sort: str, page: int) -> dict:
    return query.search(q, sort, page)
