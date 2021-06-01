from bs4 import BeautifulSoup
import requests_async as requests
from requests.exceptions import Timeout, ConnectionError
from .parsers import getText

async def getHtml(link: str, routePrincipal: str) -> dict:
    try:
        response = await requests.get(link)
        html = response.text
        text = getText(html)
        title = BeautifulSoup(html, "lxml").find("li", attrs={"class":"active"}).text
        title = str(title).rstrip().lstrip().replace("\\", " ").replace("/", " ").replace("?", "")        
        return {
            "title": title,
            "text": text
        }
    except (Timeout, ConnectionError):
        await getHtml(link, routePrincipal)