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
    with get_connection() as conn:
        for item in items:
            conn.execute("""
                INSERT OR IGNORE
                INTO disclosures 
                (pdf_url,time,code,company,title)
                VALUES(?, ?, ?, ?, ?)"""
                ,(item["pdf_url"], item["time"], item["code"], item["company"], item["title"]))

def load_disclosures() :
    with get_connection() as conn:
        conn.row_factory = sqlite3.Row
        result = conn.execute("""
                    SELECT pdf_url, time, code, company, title
                    FROM disclosures
                    """).fetchall()
    return result

def collect():
    init_db()
    results = fetch_disclosures()
    save_disclosures(results)
    print(f"collect: {len(results)} 件保存")
    return results



if __name__ == "__main__":
    results = load_disclosures()
    for item in results:
        #print(item["code"], item["company"], item["title"])
        print(item["pdf_url"], item["time"], item["code"], item["company"], item["title"])
       
    print(f"\n合計 {len(results)} 件")