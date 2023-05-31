import query
from fastapi import FastAPI

# uvicorn app:app --reload
app = FastAPI()


@app.get("/search")
def search(q: str):
    return {"results": query.search(q)}
