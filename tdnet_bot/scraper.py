import requests
from bs4 import BeautifulSoup
from datetime import date


def fetch_disclosures(target_date=None):
    d = target_date or date.today()
    url = f"https://www.release.tdnet.info/inbs/I_list_001_{d:%Y%m%d}.html"
    resp = requests.get(url, timeout=10)
    resp.encoding = "utf-8"
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


if __name__ == "__main__":
    for item in fetch_disclosures():
        print(item["code"], item["company"], item["title"])