from scraping.novel import getNovel
from scraping.chapter import getChapters
from scraping.html import getHtml
from terminal.terminal import ProcessInTerminal
from db.create_db import CreateDb

async def main():
    url = input("Insert url: ").rstrip().lstrip()

    novel = getNovel(url)
    route = "./webnovels/" + novel["title"]
    chapters_url = await getChapters(novel["chapter"])
    route = f'./webnovel/{novel["title"]}.db'
    
    db_novel = CreateDb(route=route)
    
    processInTerminal = ProcessInTerminal(
        total=len(chapters_url),
        title=novel["title"]
    )

    db_novel.insertIntoNovel(novel=novel["title"], url=url)

    for chapter_url in chapters_url:
        chapter = await getHtml(chapter_url, route)
        db_novel.insertIntoChapter(title=chapter["title"])
        db_novel.insertIntoLine(text=chapter["text"])
        processInTerminal.print()
    
if __name__ == "__main__":
    from asyncio import run
    run(main())
