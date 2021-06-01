import re
from itertools import product
from pymysql.connections import Cursor

def filter_characters(line: str, words: set):
    excludings = {'"', "'", "\\", '?', '¿', '!', '¡', '!', "$", '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', ')', '(', '}', '%', '+', '-', ':', '.', ';', '[', ']', ',', '…', '’', '‘', '~', '–', '—'}
    words_excludings = {'they', 'i', 'we', 'you', 'she', 'it', 'he', 'are', 'am', 'the', 'a', 'is', 'your', 'their', 'who', 'my', 'didnt', 'may', 'its', 'vs', 'arent', 'me', 'isnt', 'wouldnt', 'wont', 'dont', 'doesnt', 'myself', 'im', 'cant', 'an'}
    new_line = line.lower()
    for character in excludings:
        new_line = new_line.replace(character, "")
    
    set_line = set(new_line.split(" "))
    if '' in set_line:
        set_line.remove('')
    
    set_line.difference_update(words)
    set_line.difference_update(words_excludings)

    return set_line

def add_ignore_word(cursor: Cursor, word: str) -> None:
    sql = "SELECT word FROM ignore_word WHERE word=%s"
    cursor.execute(sql, word)
    
    if (len(cursor.fetchall()) == 0):
        sql = "INSERT INTO ignore_word(word) VALUES(%s)"
        cursor.execute(sql, word)
    return None

def add_excluding_character(cursor: Cursor, character: str) -> None:
    sql = "SELECT ig_char FROM excluding_character WHERE ig_char=%s"
    cursor.execute(sql, character)
    
    if (len(cursor.fetchall()) == 0):
        sql = "INSERT INTO excluding_character(ig_char) VALUES(%s)"
        cursor.execute(sql, character)
    return None

def send_titles_to_database(directories: list, cursor: Cursor) -> None:
    for directory in directories:
        sql = "SELECT * FROM novel WHERE novel=%s;"
        cursor.execute(sql, (directory["title"]))
        result = cursor.fetchall()
        
        if len(result) == 0:
            sql = "INSERT INTO novel(novel) VALUES(%s);"
            cursor.execute(sql, (directory["title"]))

def filter_text(text: str) -> set:
    list_text = re.findall(r'([A-Z][^.!?]*[.!?])' , text)
    set_text = {t for t in list_text if len(t) > 20}
    return set_text

def send_text_to_database(all_files: list, cursor: Cursor, connection):
    for chapter in all_files:
        sql = "SELECT id FROM novel WHERE novel=%s;"
        cursor.execute(sql, chapter.replace(".txt", "").split("/")[-2])
        novel_id = cursor.fetchone()["id"]
        
        chapter_title = chapter.replace(".txt", "").split("/")
        chapter_title = chapter_title[-1]
        sql = "SELECT * FROM chapter WHERE id_novel=%s AND chapter=%s;"
        cursor.execute(sql,(novel_id, chapter_title))
        result = cursor.fetchall()
        
        if len(result) == 0:
            sql = "INSERT INTO chapter(id_novel,chapter) VALUES(%s,%s);"
            cursor.execute(sql, (novel_id, chapter_title))
        
        sql = "SELECT id FROM chapter WHERE chapter=%s AND id_novel=%s;"
        cursor.execute(sql,(chapter_title, novel_id))
        
        id_chapter = cursor.fetchall()
        chapter_file = open("{}".format(chapter), "r", encoding="utf-8")
        chapter_text = filter_text(chapter_file.read())
        
        try:
            if len(cursor.fetchall()) == 0:
                sql = "INSERT INTO line(id_novel, id_chapter, line) VALUES(%s,%s,%s);"
                cursor.executemany(
                    sql, 
                    product([novel_id],
                    [id_chapter[0]["id"]],
                    chapter_text)
                )
        except Exception:
            print(sql)
        chapter_file.close()
        connection.commit()
        