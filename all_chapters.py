import subprocess
from functionalities import getNovel, searchInFolder, createFolder, getChapters, getHtml

async def main():
    link = input("Insert link: ")

    novel = getNovel(link)
    route = "./webnovels/"

    if searchInFolder(novel["title"], route):
        route = route + novel["title"]

        createFolder(route)
        chapters = await getChapters(novel["chapter"])
        total = len(chapters)
        count = 1
        
        for chapter in chapters:
            complete = await getHtml(chapter, route)

            subprocess.run("clear")
            percentage = (count / total) * 100
            print("Novel: {}\nTotal: % {:.2f} ({} of {})".format(
                                                                    novel["title"], 
                                                                    percentage, 
                                                                    count, 
                                                                    total
                                                                )
                                                            )
            count += 1                
    else:
        print("Folder was added previously")
    
if __name__ == "__main__":
    from asyncio import run
    run(main())