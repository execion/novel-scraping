from os import scandir
import pymysql.cursors
from functions import send_titles_to_database, send_text_to_database
from database import database_novel

root = "./webnovel"
dirList = [obj.name for obj in scandir(root) if obj.is_dir()]
directories = []
all_files = []

for folder in dirList:
    route_of_folder = root + "/" + folder
    temp_dict = {}
    temp_dict["title"] = folder
    directories.append(temp_dict)
    
    files_in_folder = [(route_of_folder + "/" + obj.name) for obj in scandir(route_of_folder) if obj.is_file()]
    all_files.extend(files_in_folder)

connection = pymysql.connect(
    host=database_novel["host"],
    user=database_novel["user"],
    password=database_novel["password"],
    database=database_novel["database"],
    cursorclass=pymysql.cursors.DictCursor
)

with connection:
    with connection.cursor() as cursor:
        send_titles_to_database(directories, cursor)  
        send_text_to_database(all_files, cursor, connection) 
