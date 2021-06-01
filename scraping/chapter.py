import requests_async as requests
from bs4 import BeautifulSoup

async def getChapters(link: str):
    try:
        response = await requests.get(link)
        html = response.text
        options = set(BeautifulSoup(html, "lxml").find_all("option", attrs={"class": "short"}))
        temp = []
        for option in options:
            temp.append(option["data-redirect"])
        return temp
    except ValueError:
        print("Ha sucedido un error en obtener el menu de capitulos: ", link)