from flask import Flask, request, render_template
import os

import pynput

from controll import MAUS, KEYBORD, MEDIA
from CuteON import Get_, Read_, CuteScript, Types

import webbrowser as wb

from VideoSelector import Video

app = Flask(__name__)

CONFIG = Read_.readAll("config.sws")

CURSOR_POSITION = [CONFIG["FORCE"]]
SIZE = Types.List.toInt(CONFIG["SIZE"])
CUESOR_DERECTION = ["None"]
DEFOLT_FORCE = CONFIG["FORCE"]
REQESTS = CONFIG["REQESTS"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/Video')
def video():
    Video.line("templates/Video.html", tasks=REQESTS)
    return render_template('Video.html')

@app.route('/Options')
def options():
    return render_template('Options.html')

@app.route('/ReadMe')
def readMe():
    return render_template('ReadMe.html')

# start process for index
@app.route('/', methods=['POST'])
def index_process():
    return render_template("index.html")

@app.route('/VIDEO-index', methods=['POST'])
def video_process():

    reqest = request.form['reqest']
    flag = request.form['flag']
    if flag == "open":
        wb.open(reqest)
        return render_template("index.html")
    if flag == "search":
        wb.open('https://www.youtube.com/results?search_query=' + format(reqest))
        return render_template("index.html")
    if flag == "write" and reqest != "":
        KEYBORD.write(reqest)
        return render_template("index.html")
    
    else:
        return render_template('error.html')
        
    return render_template("index.html")

@app.route('/CONTROLL-index', methods=['POST'])
def controll_process():
    system = request.form['command']
    CUESOR_DERECTION.append(system)

    force = MAUS.force(
        derection=CUESOR_DERECTION,
        force_=CURSOR_POSITION[len(CURSOR_POSITION)-1],
        defolt_force=DEFOLT_FORCE)
    
    CURSOR_POSITION.append(
        MAUS.do(system=system, force=force)
        )
    return render_template("index.html")

@app.route('/SCROLLING-index', methods=['POST'])
def scrolling_process():
    system = request.form['command']
    MAUS.scroll(system=system)
    return render_template("index.html")

@app.route('/MEDIA-index', methods=['POST'])
def MEDIA_index_process():
    media = request.form['media']
    MEDIA.do(media)
    return render_template("index.html")

@app.route('/COMMAND-index', methods=['POST'])
def COMMAND_index_process():
    system = request.form['command']
    MAUS.do(system=system)
    return render_template("index.html")
# end  process for index

# start process for Options.html
@app.route('/ROOT-options', methods=['POST'])
def root_process():
    primary_color = request.form['primary-color']
    text_color = request.form['text-color']
    background_color = request.form['background-color']
    hight_text = request.form['hight-text']
    input_text_color = request.form['input-text-color']
    
    file = open("css/root.css", "r", encoding="utf-8").read()
    root_new = ':root{\n--primary-color: '+primary_color+';\n--text-color: '+ text_color + ';\n--background-color: '+ background_color + ';\n--hight-light: ' + hight_text + ';\n--input-text-color: ' + input_text_color + ";\n--font: Arial, Helvetica, sans-serif;\n}\n/*cut*/"
    open("css/root.css", "w", encoding="utf-8").write(root_new + "\n\n\n" + file[1])
    CuteScript.ConveyorBuilding(Read_.readLine("config.sws", "BP-FILE"))
    return render_template("Options.html")

# end process for Options.html

# start process for Video.html
@app.route('/VIDEO-video', methods=['POST'])
def VIDEO_video_process():
    video = request.form['video']
    try:
        wb.open(video)
        return render_template("index.html")
    except:
        pass
    return render_template("Video.html")

# end process for Video.html

if __name__ == '__main__':
    CuteScript.ConveyorBuilding(Read_.readLine("config.sws", "BP-FILE"))
    app.run(host="0.0.0.0", port=8080)