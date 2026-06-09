from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from tdnet_bot.scraper import fetch_disclosures

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
    return fetch_disclosures()