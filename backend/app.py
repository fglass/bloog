import query
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# uvicorn app:app --reload
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
def search(q: str):
    return {"results": query.search(q)}
