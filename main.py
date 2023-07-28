from flask import Flask, request, render_template, jsonify
from CMFIO import loger, Compilator, element
import webbrowser as wb
from pynput import mouse, keyboard

import time

import os

app = Flask(__name__)

files_template = [
    "index.html",
    "YouTube.html",
    "error.html",
    "add_element.html",
    "keybord.html",
    "options.html",
    "dev.html",
    "logs.html"
]

def comp_files(files):
    for i in files:
        Compilator.build(i)
    loger.send(status="succes", title="Сборка завершина", description="Все файлы были собраны успешно, интеграция стилей завершина")

# сборка всех шаблонав по средствам сборщика html файлов
comp_files(files_template)

@app.route('/logs')
def logs():  
    return render_template('logs.html')

@app.route('/')
def index():  
    return render_template('index.html')

@app.route('/index', methods=['POST'])
def index_process():
    adres = request.form['adres']
    if adres != "":
        wb.open(adres)
        return render_template('index.html')
    else:
        return adres

@app.route('/youtube')
def youtube():  
    return render_template('YouTube.html')

@app.route('/youtube', methods=['POST'])
def youtube_process():
    reqest = request.form['reqest']
    video = request.form['video']

    if video != "":
        wb.open(video)
        return render_template('YouTube.html')
        
    if reqest != "":
        wb.open('https://www.youtube.com/results?search_query=' + format(reqest))
        return render_template('YouTube.html')
    
    else:
        loger.send(status="error", title="Поиск в Ютуб", description="Вы не запонели не одно из полей, первое поле для поиска на ютубе, второе поле для открытия ссылки")
        return render_template('error.html')

@app.route('/search', methods=['POST'])
def yandex_process():
    
    search = request.form['search']
    comm = request.form['command']

    if comm == "close":
        from pynput.keyboard import Key, Controller
        keyboard = Controller() #контроллер миши 
        keyboard.press(Key.alt)
        keyboard.press(Key.f4)
        keyboard.release(Key.f4)
        keyboard.release(Key.alt)
        return render_template('index.html')

    if search == ".dev" and comm == "search":
        return render_template('dev.html')

    if search != "" and comm == "search":
        wb.open('https://yandex.ru/search/?text=' + format(search))
        return render_template('index.html')
    
    else:
        loger.send(status="error", title="Невозможно найти", description="Указыный запрос евляется пустым, заполните текстовое поле")
        return render_template('error.html')
    
@app.route('/input-key', methods=['POST'])
def input_process():
    from pynput.keyboard import Key, Controller
    keyboard = Controller()
    text = request.form['text']
    insert = request.form['insert']


    if text != "" and insert == "true":
        keyboard.type(text)
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
        return render_template('keybord.html')
    
    else:
        loger.send(status="error", title="Что писать?", description="Невозможно написать пустую сроку!")
        return render_template('error.html')

@app.route('/media', methods=['POST'])
def media_process():

    media = request.form['media']
    from pynput.keyboard import Key, Controller
    keyboard = Controller() #контроллер клавы
    if media == "play":
        keyboard.press(Key.space)
        keyboard.release(Key.space)
        return render_template('YouTube.html')
    if media == "full":
        keyboard.press('f')
        keyboard.release('f')
        return render_template('YouTube.html')
    if media == "c":
        keyboard.press('c')
        keyboard.release('c')
        return render_template('YouTube.html')
    if media == "mute":
        keyboard.press('m')
        keyboard.release('m')
        return render_template('YouTube.html')
    if media == "next":
        keyboard.press(Key.shift)
        keyboard.press('n')
        keyboard.release('n')
        keyboard.release(Key.shift)
        return render_template('YouTube.html')
    if media == "close":
        keyboard.press(Key.alt)
        keyboard.press(Key.f4)
        keyboard.release(Key.f4)
        keyboard.release(Key.alt)
        return render_template('YouTube.html')   
    else:
        loger.send(status="error", title="Неизвестная комманда", description="Комманда упровления не звестна, проверте правельность атрибута <i>value</i>")
        return render_template('error.html')
    
@app.route('/element')
def add_element():  
    return render_template('add_element.html')

@app.route('/element', methods=['POST'])
def add_element_process():
    url = request.form['url']
    text = request.form['text']
    if text == "" or url == "":
        loger.send(status="error", title="Ошибка элемента", description="Вы не заполнели все текстовые поля, элемент не добавлен")
        return render_template('error.html')
    else:
        return element('<button type="submit" value="' + url + '" name="adres">'+ text +'</button>\n<cut>')

@app.route('/root')
def root():  
    return render_template('options.html')

@app.route('/root', methods=['POST'])
def root_process():
    primary_color = request.form['primary-color']
    text_color = request.form['text-color']
    background_color = request.form['background-color']
    hight_text = request.form['hight-text']
    input_text_color = request.form['input-text-color']
    
    file = open("ui/ui.css", "r", encoding="utf-8").read().split("/*cut*/")
    root_new = ':root{\n--primary-color: '+primary_color+';\n--text-color: '+ text_color + ';\n--background-color: '+ background_color + ';\n--hight-light: ' + hight_text + ';\n--input-text-color: ' + input_text_color + ";\n--font: Arial, Helvetica, sans-serif;\n}\n/*cut*/"
    open("ui/ui.css", "w", encoding="utf-8").write(root_new + "\n\n\n" + file[1])
    comp_files(files_template)
    return render_template('options.html')
"""
:root{
    --primary-color: #00dc8c;
    --text-color: #141414;
    --background-color: #36393e;
    --card-bg: #46493e;
    --font: Arial, Helvetica, sans-serif;
    --acttent-text: #28a08c;
    --hight-light: #28a08cff;
    --head-color: #141414;
    --input-text-color: #ebebeb;
}
"""

@app.route('/color-gam', methods=['POST'])
def gamma_process():
    gamma = request.form['set']
    file = open("ui/" + gamma, "r", encoding="utf-8").read()
    open("ui/ui.css", "w", encoding="utf-8").write(file)
    comp_files(files_template)
    return render_template('index.html')

@app.route('/keybord')
def keybord():  
    return render_template('keybord.html')

@app.route('/keybord', methods=['POST'])
def keybord_process():
    system = request.form['command']
    force = 100
    from pynput.mouse import Button, Controller
    mouse = Controller() #контроллер миши 

    if system == "off":
        os.system("shutdown -h")
        return render_template('keybord.html')
    if system == "up":
        mouse.move(0, -force)
        return render_template('keybord.html')
    if system == "left":
        mouse.move(-force, 0)
        return render_template('keybord.html')
    if system == "right":
        mouse.move(force, 0)
        return render_template('keybord.html')
    if system == "down":
        mouse.move(0, force)
        return render_template('keybord.html')
    if system == "mouse-right":
        mouse.press(Button.right)
        mouse.release(Button.right)
        return render_template('keybord.html')
    if system == "mouse-left":
        mouse.press(Button.left)
        mouse.release(Button.left)
        return render_template('keybord.html')
    if system == "skroll-up":
        mouse.scroll(0, 2)
        return render_template('keybord.html')
    if system == "skroll-down":
        mouse.scroll(0, -2)
        return render_template('keybord.html')
    if system == "volume+":
        from pynput.keyboard import Key, Controller
        keyboard = Controller() #контроллер клавы
        keyboard.press(Key.media_volume_up)
        keyboard.release(Key.media_volume_up)
        return render_template('keybord.html')
    if system == "volume-":
        from pynput.keyboard import Key, Controller
        keyboard = Controller() #контроллер клавы
        keyboard.press(Key.media_volume_down)
        keyboard.release(Key.media_volume_down)
        return render_template('keybord.html')   
    else:
        print(system)
        return render_template('keybord.html')

@app.route('/media-pad', methods=['POST'])
def media_pad_process():

    media = request.form['media']
    from pynput.keyboard import Key, Controller
    keyboard = Controller() #контроллер клавы
    if media == "play":
        keyboard.press(Key.space)
        keyboard.release(Key.space)
        return render_template('keybord.html')
    if media == "full":
        keyboard.press('f')
        keyboard.release('f')
        return render_template('keybord.html')
    if media == "c":
        keyboard.press('c')
        keyboard.release('c')
        return render_template('keybord.html')
    if media == "mute":
        keyboard.press('m')
        keyboard.release('m')
        return render_template('keybord.html')
    if media == "next":
        keyboard.press(Key.shift)
        keyboard.press('n')
        keyboard.release('n')
        keyboard.release(Key.shift)
        return render_template('keybord.html')
    if media == "close":
        keyboard.press(Key.alt)
        keyboard.press(Key.f4)
        keyboard.release(Key.f4)
        keyboard.release(Key.alt)
        return render_template('keybord.html')   
    else:
        loger.send(status="error", title="Неизвестная комманда", description="Комманда упровления не звестна, проверте правельность атрибута <i>value</i>")
        return render_template('error.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)