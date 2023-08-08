from youtubesearchpython import *

import hashlib

class BUILD():

    def send(status="succes", title="some log", description="simple log", log_form="template/video_element.html", log_jurnal="templates/Video.html"):
        log_file = []
        file = open(log_form, "r", encoding="utf-8").read().split("<log>")
        log_script = file[1].split("</log>")
        ctx = log_script[0].split()
        if "!title" in ctx:
            log_file.append('<h1 class="' + status + '">'+ title + "</h1>")
        if  "!description" in ctx:
            log_file.append('<p>'+ description + "</p>")
        log = file[0] + "\n".join(log_file) + log_script[1] + "<cut>"
        f = open(log_jurnal, "r", encoding="utf-8").read().split("<cut>")
        try:
            open(log_jurnal, "w", encoding="utf-8").write(f[0] + log + f[1])
        except:
            pass

def comp(file, img, link, title):
    
    ctx = open(file, "r", encoding="utf-8").read().split("<cut>")

    content = open("template/video_element.html", "r", encoding="utf-8").read().split("\n")
    arr = []
    for i in content:
        if i == "img:":
            arr.append('<a href="' + link + '"><img class="project-img" src="' + img + '"></a>')
        if i == "title:":
            arr.append("<h1>" + title + "</h1>")
        if i == "link:":
            arr.append('<button type="submit" name="video" value="' + link + '" class="show">Смотреть</button>')
        else:
            arr.append(i)
    for i in arr:
        if i == "title:" or i == "img:":
            arr.remove(i)
    
    open(file, "w", encoding="utf-8").write(ctx[0] + "\n".join(arr)+ "\n\n<cut>" + ctx[1])

class Video():

    def line(file, tasks, Size=5):
        for task in tasks:
            customSearch = CustomSearch(task, VideoUploadDateFilter.thisYear, limit = Size)
        
            for i in range(Size):
                link = (customSearch.result()['result'][i]['link'])
                title = (customSearch.result()['result'][i]['title'])
                thumbnails = (customSearch.result()['result'][i]['thumbnails'][0]["url"])
                comp(file, thumbnails, link, title)

