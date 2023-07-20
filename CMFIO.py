
DIR = "template/"
command = ["#include", "#insert", "#line"]

import time

import CuteON

from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps

import requests

from bs4 import BeautifulSoup

def joyreactor(url, task):
    arr = []
    URL = url + task
    HEDERS = {
            'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        }

    response = requests.get(URL, HEDERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    items = soup.findAll('div', class_ = 'image')
    comps = []
    v_l = []

    for item in items:
        comps.append({'link': item.find('img', class_ = '').get('src')})
    for comp in comps:
        v_l.append(comp['link'])
    print(v_l)
    try:
        for i in v_l:
            arr.append('<img src="http:' + i + '">')
    except:
        pass
    return "<br>".join(arr)

def Other(url, task):
    arr = []
    URL = url + "/" + task
    HEDERS = {
            'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        }

    response = requests.get(URL, HEDERS)
    soup = BeautifulSoup(response.content, 'html.parser')
    items = soup.findAll('div', class_ = 'box')
    comps = []
    v_l = []

    for item in items:
        comps.append({'link': item.find('a', class_ = 'boxInner').get('href')})
    for comp in comps:
        v_l.append(comp['link'])
    print(v_l)
    try:
        for i in v_l:
            arr.append('<a href="' + url + i + '">' + i + '</a>')
    except:
        pass
    return "<br>".join(arr)

def Redit(reqest):

    # Отправляем GET-запрос к главной странице Reddit
    url = 'https://www.reddit.com/search/?q=' + reqest
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
    response = requests.get(url, headers=headers)
    arr = []
    v_l = []
    t_l = []

    # Создаем объект BeautifulSoup для парсинга HTML-кода
    soup = BeautifulSoup(response.text, 'html.parser')

    # Ищем элементы с классом "Post" (посты) и извлекаем заголовки и ссылки
    post_elements = soup.find_all('div', class_='_2n04GrCyhhQf-Kshn7akmH _19FzInkloQSdrf0rh3Omen')
    for post in post_elements:
        title_element = post.find('h3', class_='_eYtD2XCVieq6emjKBH3m')
        title = title_element.text.strip() if title_element else 'No Title'

        link_element = post.find('a', class_='')
        link = link_element['href'] if link_element else '#'

        print(f'Title: {title}')
        print(f'Link: {link}')
        print('---')
        v_l.append(link)
        t_l.append(title)
    try:
        c = 0
        for i in v_l:
            arr.append('<a href="' + "https://www.reddit.com" + i + '">' + t_l[c] + '</a>')
            c += 1
    except:
        pass
    return "<br><br>".join(arr)

def Temp():
    owm = OWM('88c77e859289463928b17b24f2f7ea99')
    mgr = owm.weather_manager()
    observation = mgr.weather_at_place('Молдова')
    w = observation.weather
    w2 = w.temperature('celsius')['temp']
    print(w)
    print(w2)
    return str(w.temperature('celsius')['temp']) + '°С'

def element(element):
    ctx = open("template/index.html", "r", encoding="utf-8").read().split("<cut>")
    open("template/index.html", "w", encoding="utf-8").write(ctx[0] + element + ctx[1])

class Compilator:

    def widget(paph_widgets : str, bone : str, data="data.sws") -> str:

        File = open("template/" + bone, "r").read()
        Text = File.split("\n")
        fin = []

        count = 0
        
        for i in Text:
            print(i)
            word = i.split()
            try:
                print(word[0])
                if word[0] == "#include":
                    name_file = word[1].split(".")
                    if name_file[1] == "css":
                        print("ok")
                        fin.append("<style>\n" + open(word[1], "r").read() + "\n" + "</style>\n")
                        del Text[count]
                    if name_file[1] == "js":
                        fin.append("<script>\n" + open(word[1], "r").read() + "\n" + "</script>\n")
                        del Text[count]

                if word[0] == "#insert":
                    name_file = word[1].split(".")
                    if name_file[1] == "html":
                        print("ok")
                        fin.append(open(word[1], "r").read() + "\n")
                        del Text[count]           
                else:
                    fin.append(i)
            except:
                fin.append(i)
            
            count += 1

        File = ("\n".join(fin)).split("<cut>")

        text = []

        for i in paph_widgets:
            contnet = open("widgets/" + i, "r", encoding="utf-8").read()
            TEGS = [contnet.split("\n")[0], contnet.split("\n")[len(contnet.split("\n"))-1]] 
            arr = []
            c = contnet.split("\n")

            for t in c:
                for q in t.split():

                    if q == "say:":
                        ctx = t.split()[t.split().index(q) + 1]

                        f = t.split("say: " + ctx)
                        txt = []
                        for j in ctx.split("_"):
                            txt.append(j)

                        arr.append(f[0] + " ".join(txt) + f[1])

                    if q == "data:":
                        ctx = t.split()[t.split().index(q) + 1]

                        f = t.split("data: " + ctx)
                        arr.append(f[0] + CuteON.Get_.getLine(data, ctx) + f[1])

                    if q == "redit:":
                        ctx = t.split()[t.split().index(q) + 1]

                        f = t.split("redit: " + ctx)
                        arr.append(f[0] + Redit(ctx) + f[1])

                    if q == "parser:":
                        url = t.split()[t.split().index(q) + 1]
                        ctx = t.split()[t.split().index(q) + 2]

                        f = t.split("parser: " + url + " " + ctx)
                        arr.append(f[0] + Other(url, ctx) + f[1])

                    if q == "joyreactor:":
                        url = t.split()[t.split().index(q) + 1]
                        ctx = t.split()[t.split().index(q) + 2]

                        f = t.split("joyreactor: " + url + " " + ctx)
                        arr.append(f[0] + joyreactor(url, ctx) + f[1])

                    if q == "time:":

                        f = t.split("time:")
                        arr.append(f[0] + time.strftime("%H:%M") + f[1])

                    if q == "temp:":

                        f = t.split("temp:")
                        arr.append(f[0] + Temp() + f[1])

            text.append(TEGS[0] + "\n" + "\n".join(arr) + "\n" + TEGS[1])


        return "\n".join(fin)
        

    def comp(file, file_out):
        text = open(DIR + file, "r", encoding="utf-8").read()
        Text = text.split("\n")
        fin = []
        count = 0
        for i in Text:
            print(i)
            word = i.split()
            try:
                print(word[0])
                if word[0] == "#include":
                    name_file = word[1].split(".")
                    if name_file[1] == "css":
                        print("ok")
                        fin.append("<style>\n" + open(word[1], "r").read() + "\n" + "</style>\n")
                        del Text[count]
                    if name_file[1] == "js":
                        fin.append("<script>\n" + open(word[1], "r").read() + "\n" + "</script>\n")
                        del Text[count]

                if word[0] == "#insert":
                    name_file = word[1].split(".")
                    if name_file[1] == "html":
                        print("ok")
                        fin.append(open(word[1], "r").read() + "\n")
                        del Text[count]

                if word[0] == "#line":
                    name_file = word[1].split(".")
                    if name_file[1] == "html":
                        print("ok")
                        WIDGET = Compilator.widget(CuteON.Get_.getAll("template/CFG.sws"), "main.html", "card.html")
                        fin.append(open(word[1], "r").read() + "\n")
                        del Text[count]       
                else:
                    fin.append(i)
            except:
                fin.append(i)

            count += 1
            open(file_out, "w", encoding="utf-8").write("\n".join(fin))
    

    def build(file):
        text = open(DIR + file, "r", encoding="utf-8").read()
        Text = text.split("\n")

        fin = []

        count = 0

        for i in Text:

            word = i.split()
            try:
               
                if word[0] == "#include":

                    name_file = word[1].split(".")
                    if name_file[1] == "css":
                        print("ok")
                        fin.append("<style>\n" + open(word[1], "r").read() + "\n" + "</style>\n")
                        del Text[count]

                    if name_file[1] == "js":
                        fin.append("<script>\n" + open(word[1], "r").read() + "\n" + "</script>\n")
                        del Text[count]        

                if word[0] == "#insert":
                    name_file = word[1].split(".")
                    if name_file[1] == "html":
                        print("ok")
                        fin.append(open(word[1], "r", encoding="utf-8").read() + "\n")
                        del Text[count]  

                else:
                    fin.append(i)

            except:
                fin.append(i)
            count += 1
        try:
            for i in fin:
                if i.split()[0] in command:
                    del fin[fin.index(i)]
        except:
            pass

        open("templates/" + file, "w", encoding="utf-8").write("\n".join(fin))
            
    
                