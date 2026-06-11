import requests
from bs4 import BeautifulSoup
from datetime import date


def fetch_page(d, page):
    """指定日・指定ページの開示一覧を取得する。1件も無ければ空リストを返す。"""
    url = f"https://www.release.tdnet.info/inbs/I_list_{page:03d}_{d:%Y%m%d}.html"
    resp = requests.get(url, timeout=10)
    resp.encoding = "utf-8"

    # 存在しないページは404になることがあるので確認
    if resp.status_code != 200:
        return []

    soup = BeautifulSoup(resp.text, "html.parser")

    disclosures = []
    for row in soup.select("tr"):
        cols = row.select("td")
        if len(cols) < 4:
            continue
        link_tag = cols[3].select_one("a")
        if not link_tag:
            continue
        disclosures.append({
            "time": cols[0].text.strip(),
            "code": cols[1].text.strip()[:4],
            "company": cols[2].text.strip(),
            "title": cols[3].text.strip(),
            "pdf_url": link_tag.get("href", ""),
        })
    return disclosures


def fetch_disclosures(target_date=None):
    """全ページを巡回して、その日の開示をすべて取得する。"""
    d = target_date or date.today()
    all_disclosures = []
    page = 1
    while True:
        items = fetch_page(d, page)
        if not items:          # 空ページ＝最終ページの次なので終了
            break
        all_disclosures.extend(items)
        page += 1
    return all_disclosures