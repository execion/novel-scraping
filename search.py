import pymysql.cursors
from database import database_word

word_database = pymysql.connect(
    host=database_word["host"],
    user=database_word["user"],
    password=database_word["password"],
    database=database_word["database"],
    cursorclass=pymysql.cursors.DictCursor
)

with word_database:
    with word_database.cursor() as cursor:
        listTypeWord = ['adverb', 'adjective', 'noun', 'verb', 'irregular_verb', 'preposition', 'linking_word']
        while True:
            word = input("\nInsert word for search: ").rstrip().lstrip().lower()
            if(word == "-exit"):
                break
            
            for typeWord in listTypeWord:
                sql = 'SELECT word FROM {} WHERE word="{}"'.format(typeWord, word)
                cursor.execute(sql)
                results = cursor.fetchall()

                if (len(results) >= 1):
                    results = " ".join([result["word"] for result in results])
                    print("{}:".format(typeWord.capitalize()), results)
                else:
                    print("{}: 0".format(typeWord))
            
            word_database.commit()