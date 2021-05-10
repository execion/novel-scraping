from os import scandir
import subprocess
from itertools import product
from os.path import join
import pymysql.cursors
from functionalities import filterText
from database import database_novel

root = "./webnovel"
dirList = [obj.name for obj in scandir(root) if obj.is_dir()]
directories = []
files = []

for folder in dirList:
    temp_route = root + "/" + folder
    temp_dict = {}
    temp_dict["title"] = folder
    directories.append(temp_dict)
    files_temp = [(temp_route + "/" + obj.name) for obj in scandir(temp_route) if obj.is_file()]
    files.extend(files_temp)

connection = pymysql.connect(
    host=database_novel["host"],
    user=database_novel["user"],
    password=database_novel["password"],
    database=database_novel["database"],
    cursorclass=pymysql.cursors.DictCursor
)

total = len(files)
count = 1

with connection:
    with connection.cursor() as cursor:
        for directory in directories:
            sql = "SELECT * FROM novel WHERE novel=%s;"
            cursor.execute(sql, (directory["title"]))
            result = cursor.fetchall()
            
            if len(result) == 0:
                sql = "INSERT INTO novel(novel) VALUES(%s);"
                cursor.execute(sql, (directory["title"]))
        
        for chapter in files:
            subprocess.run("clear")
            percentage = (count / total) * 100
            print("Total: % {:.2f} ({} of {})".format(percentage, count, total))
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
                cursor.execute(sql, (novel_id, chapter_title) )
                sql = "SELECT id FROM chapter WHERE chapter=%s AND id_novel=%s;"
                cursor.execute(sql,(chapter_title, novel_id))
                
                id_chapter = cursor.fetchall()
                chapter_file = open("{}".format(chapter), "r", encoding="utf-8")
                chapter_text = filterText(chapter_file.read())
                
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
            elif len(result) == 1:
                sql = "SELECT id FROM chapter WHERE chapter=%s AND id_novel=%s;"
                cursor.execute(sql,(chapter_title, novel_id))
                
                id_chapter = cursor.fetchall()
                chapter_file = open("{}".format(chapter), "r", encoding="utf-8")
                chapter_text = filterText(chapter_file.read())
                
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
            
            count += 1 
            connection.commit()
            
                