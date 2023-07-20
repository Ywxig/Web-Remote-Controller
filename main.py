from flask import Flask, request, render_template, jsonify
import CMFIO
import webbrowser as wb
from pynput import mouse, keyboard


from youtube import *
import os




app = Flask(__name__)

# сборка всех шаблонав по средствам сборщика html файлов
CMFIO.Compilator.build("index.html")
CMFIO.Compilator.build("YouTube.html")
CMFIO.Compilator.build("error.html")
CMFIO.Compilator.build("add_element.html")
CMFIO.Compilator.build("keybord.html")

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
        keyboard.press('F')
        keyboard.release('F')
        return render_template('YouTube.html')
    if media == "c":
        keyboard.press('C')
        keyboard.release('C')
        return render_template('YouTube.html')
    if media == "mute":
        keyboard.press('M')
        keyboard.release('M')
        return render_template('YouTube.html')
    if media == "next":
        keyboard.press(Key.shift)
        keyboard.press('N')
        keyboard.release('N')
        keyboard.release(Key.shift)
        return render_template('YouTube.html')
    if media == "close":
        keyboard.press(Key.alt)
        keyboard.press(Key.f4)
        keyboard.release(Key.f4)
        keyboard.release(Key.alt)
        return render_template('YouTube.html')   
    else:
        return render_template('error.html')
    
@app.route('/element')
def add_element():  
    return render_template('add_element.html')

@app.route('/element', methods=['POST'])
def add_element_process():
    url = request.form['url']
    text = request.form['text']
    if text == "" or url == "":
        return render_template('error.html')
    else:
        return CMFIO.element('<button type="submit" value="' + url + '" name="adres">'+ text +'</button>\n<cut>')

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
    else:
        print(system)
        return render_template('keybord.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)