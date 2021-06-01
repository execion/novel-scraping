import re
from bs4 import BeautifulSoup

def getText(html: str) -> list:
    try:
        div_container = BeautifulSoup(html, "lxml").find("div", attrs={"class": "read-container"}).text
        paragraph = BeautifulSoup(div_container, "lxml").find_all("p",attrs={"class": ""})
        text = ""
        if(len(paragraph) == 1):
            text = paragraph[0].text
        elif (len(paragraph) > 1):
            temp = [p.text for p in paragraph if len(p) > 3]
            text = "\n".join(temp)
        if len(text) > 0:
            return text_to_list(text)
        else:
            raise ValueError("The text wasn't searched")
    except ValueError:
        print("Ha sucedido un error en obtener el texto del html", "\n{}".format(html))

def text_to_list(text: str) -> list:
    texts_raw = re.findall(r'([A-Z][^.!?]*[.!?])' , text)
    texts_cleam = list({t for t in texts_raw if len(t) > 20})
    return texts_cleam