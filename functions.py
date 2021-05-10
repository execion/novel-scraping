from pymysql.connections import Cursor

def filterCharacters(line: str, words: set):
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

if __name__ == "__main__":
    import pymysql.cursors
    words_excludings = {'they', 'i', 'we', 'you', 'she', 'it', 'he', 'are', 'am', 'the', 'a', 'is', 'your', 'their', 'who', 'my', 'didnt', 'may', 'its', 'vs', 'arent', 'me', 'isnt', 'wouldnt', 'wont', 'dont', 'doesnt', 'myself', 'im', 'cant', 'an'}
    excludings = {'"', "'", "\\", '?', '¿', '!', '¡', '!', "$", '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', ')', '(', '}', '%', '+', '-', ':', '.', ';', '[', ']', ',', '…', '’', '‘', '~', '–', '—'}

    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="word",
        cursorclass=pymysql.cursors.DictCursor
    )
    with connection:
        with connection.cursor() as cursor:
            for word in excludings:
                add_excluding_character(cursor, word)
            connection.commit()
