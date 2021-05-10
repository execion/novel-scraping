import pymysql.cursors
from database import database_word

connection = pymysql.connect(
    host=database_word["host"],
    user=database_word["user"],
    password=database_word["password"],
    database=database_word["database"],
    cursorclass=pymysql.cursors.DictCursor
)

listTypeWord = ["adverb", "adjective", "noun", "verb", "irregular_verb", "preposition", "linking_word"]

with connection:
    with connection.cursor() as cursor:
        typeWord = input("Insert type of word: ").lstrip().rstrip().lower()

        while typeWord not in listTypeWord:
            typeWord = input("Insert type of word: ").strip().lower() 
        
        word = input("Insert word: ").lower().rstrip().lstrip()
            
        if(word != "" or word != " "):
            cursor.execute("SELECT * FROM {} WHERE word='{}';".format(typeWord,word))
            res = cursor.fetchall()

            if (len(res) == 0):
                sql = "INSERT INTO {}(word) VALUES('{}');".format(typeWord,word)
                cursor.execute(sql)
                print("Saved")
            else:
                print("Word exist in the database")
            connection.commit()
            