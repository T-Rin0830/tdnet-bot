from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from tdnet_bot.db import load_disclosures

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # 開発中はすべてのオリジンを許可
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Hello, TDnet Bot"}


@app.get("/api/disclosures")
def get_disclosures():
    return [dict(row) for row in load_disclosures()]