import pymysql.cursors
from functions import filter_characters, add_ignore_word
from database import database_word, database_novel

word_database = pymysql.connect(
    host=database_word["host"],
    user=database_word["user"],
    password=database_word["password"],
    database=database_word["database"],
    cursorclass=pymysql.cursors.DictCursor
)

set_words_clean = set()

with word_database:
    with word_database.cursor() as cursor:
        listTypeWord = ["adverb", "adjective", "noun", "verb", "irregular_verb", "preposition", "linking_word", "ignore_word"]
        list_words_unclean = []
        
        for table in listTypeWord:
            sql = "SELECT word FROM {}".format(table)
            cursor.execute(sql)
            words = cursor.fetchall()
            list_words_unclean.extend(words)
        

        for word in list_words_unclean:
            set_words_clean.add(word["word"])

        word_database.commit()

connection = pymysql.connect(
    host=database_novel["host"],
    user=database_novel["user"],
    password=database_novel["password"],
    database=database_novel["database"],
    cursorclass=pymysql.cursors.DictCursor
)

new_words = set()

with connection:
    with connection.cursor() as cursor:
        count = 0
        while len(new_words) <= 10:
            sql = "SELECT line FROM line LIMIT {}, 10".format(count)
            cursor.execute(sql)

            results = cursor.fetchall()

            for line in results:
                line = filter_characters(line["line"], set_words_clean)
                new_words.symmetric_difference_update(line)
            count += 10
            connection.commit()

ignore_word = set()

for word in new_words:
    print("Word: {}".format(word))
    action_word = int(input("Ignore = 0 ; Exit = 10 ; Continue = Other: "))
    if (action_word == 10):
        break
    elif (action_word == 0):
        ignore_word.add(word)
        
word_database = pymysql.connect(
    host=database_word["host"],
    user=database_word["user"],
    password=database_word["password"],
    database=database_word["database"],
    cursorclass=pymysql.cursors.DictCursor
)

with word_database:
    with word_database.cursor() as cursor:
        for word in ignore_word:
            add_ignore_word(cursor, word)
        word_database.commit()