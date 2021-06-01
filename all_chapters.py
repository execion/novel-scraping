import sqlite3
from itertools import product
from scraping.novel import getNovel
from scraping.chapter import getChapters
from scraping.html import getHtml
from terminal.terminal import ProcessInTerminal

async def main():
    link = input("Insert link: ").rstrip().lstrip()

    novel = getNovel(link)
    route = "./webnovels/" + novel["title"]
    chapters_url = await getChapters(novel["chapter"])

    processInTerminal = ProcessInTerminal(total=len(chapters_url), title=novel["title"])
    
    conn = sqlite3.connect(f'./webnovel/{novel["title"]}.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("CREATE TABLE novel(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, name TEXT NOT NULL, url TEXT NOT NULL)")
    cursor.execute("CREATE TABLE chapter(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, id_novel INTEGER NOT NULL, chapter TEXT NOT NULL)")
    cursor.execute("CREATE TABLE line(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, id_novel INTERGER NOT NULL, id_chapter INTEGER NOT NULL, line TEXT NOT NULL)")
    cursor.execute("INSERT INTO novel(name, url) VALUES(?, ?)", (novel["title"], link))
    cursor.execute("SELECT * FROM novel")
    novel_db = [dict(row) for row in cursor.fetchall()][0]

    for chapter_url in chapters_url:
        chapter = await getHtml(chapter_url, route)
        cursor.execute("INSERT INTO chapter(id_novel, chapter) VALUES(?, ?)", (novel_db["id"], chapter["title"]))
        cursor.execute("SELECT * FROM chapter WHERE chapter='{}'".format(chapter["title"]))
        chapter_db = [dict(row) for row in cursor.fetchall()][0]

        all = product([chapter_db["id_novel"]], [chapter_db["id"]], chapter["text"])
        cursor.executemany("INSERT INTO line(id_novel, id_chapter, line) VALUES (?, ?, ?)", all)
        processInTerminal.print()
        conn.commit()
    
if __name__ == "__main__":
    from asyncio import run
    run(main())
