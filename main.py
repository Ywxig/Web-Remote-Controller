from flask import Flask, request, render_template, jsonify
import CMFIO
import webbrowser as wb
import pyautogui as gui
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

    if media == "play":
        gui.keyDown('k')
        gui.keyUp('k')
        return render_template('YouTube.html')
    if media == "full":
        gui.keyDown('f')
        gui.keyUp('f')
        return render_template('YouTube.html')
    if media == "c":
        gui.keyDown('c')
        gui.keyUp('c')
        return render_template('YouTube.html')
    if media == "mute":
        gui.keyDown('m')
        gui.keyUp('m')
        return render_template('YouTube.html')
    if media == "next":
        gui.keyDown('Shift')
        gui.keyDown('n')
        gui.keyUp('n')
        gui.keyUp('Shift')
        return render_template('YouTube.html')
    if media == "close":
        gui.keyDown('alt')
        gui.keyDown('f4')
        gui.keyUp('f4')
        gui.keyUp('alt')
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

    if system == "off":
        os.system("shutdown -h")
        return render_template('keybord.html')
    if system == "up":
        gui.moveRel(xOffset=0, yOffset=-force)
        return render_template('keybord.html')
    if system == "left":
        gui.moveRel(xOffset=-force, yOffset=0)
        return render_template('keybord.html')
    if system == "right":
        gui.moveRel(xOffset=force, yOffset=0)
        return render_template('keybord.html')
    if system == "down":
        gui.moveRel(xOffset=0, yOffset=force)
        return render_template('keybord.html')
    if system == "mouse-right":
        gui.dragRel(xOffset=1, yOffset=0, button='right')
        return render_template('keybord.html')
    if system == "mouse-left":
        gui.dragRel(xOffset=1, yOffset=0, button='left')
        return render_template('keybord.html')
    else:
        print(system)
        return render_template('keybord.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)