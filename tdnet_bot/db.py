import sqlite3
from pathlib import Path
from tdnet_bot.scraper import fetch_disclosures

# DBファイルの置き場所（プロジェクト直下に disclosures.db を作る）
DB_PATH = Path(__file__).resolve().parent.parent / "disclosures.db"


def get_connection():
    """DBへの接続を返す。"""
    return sqlite3.connect(DB_PATH)


def init_db():
    """テーブルが無ければ作る。"""
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS disclosures (
                pdf_url  TEXT PRIMARY KEY,
                time     TEXT,
                code     TEXT,
                company  TEXT,
                title    TEXT
            )
        """)

def save_disclosures(items):
    existing_urls = load_existing_urls()
    new_items = [item for item in items if item["pdf_url"] not in existing_urls]
    with get_connection() as conn:
        for item in new_items:
            conn.execute("""
                INSERT OR IGNORE
                INTO disclosures 
                (pdf_url,time,code,company,title)
                VALUES(?, ?, ?, ?, ?)"""
                ,(item["pdf_url"], item["time"], item["code"], item["company"], item["title"]))
    return new_items


def load_disclosures() :
    with get_connection() as conn:
        conn.row_factory = sqlite3.Row
        result = conn.execute("""
                    SELECT pdf_url, time, code, company, title
                    FROM disclosures
                    """).fetchall()
    return result

def load_existing_urls():
    with get_connection() as conn:
        result = conn.execute("""
                    SELECT pdf_url
                    FROM disclosures
                    """).fetchall()
        return {data[0] for data in result}
    

def collect():
    init_db()
    results = fetch_disclosures()
    save_disclosures(results)
    return results



if __name__ == "__main__":
    results = collect()
    ##print(item["pdf_url"], item["time"], item["code"], item["company"], item["title"])
       
    #print(f"\n合計 {len(results)} 件")