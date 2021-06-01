import requests as rq
from bs4 import BeautifulSoup

def getNovel(url: str) -> dict:
    response = rq.get(url)
    data = response.text
    header = BeautifulSoup(data, "lxml").find("h3")
    title = header.text.replace("NEW", "").replace("HOT", "").replace(":", " ").rstrip().lstrip()
    chapter = BeautifulSoup(data, "lxml").find("li", attrs={"class": "wp-manga-chapter"}).a["href"]
    return {"title": title, "chapter": chapter}