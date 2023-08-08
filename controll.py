import os

from CuteON import Types

class MAUS:
    from pynput.mouse import Button, Controller
    mouse = Controller() #контроллер миши

    def force(derection, force_, min_force=20, step=10, size=[100,50], defolt_force=100) -> int:
        if derection[len(derection) - 1] == derection[len(derection) - 2]:
            print(force_)
            force = force_ * 1.5

        elif derection[len(derection) - 1] != derection[len(derection) - 2]:
            force_ = defolt_force
            if force_ < min_force or force_ > size[1]/2:
                force = force_
            else:
                force = force_ - step
        
        return force

    def scroll(system):
        if system == "skroll-up":
            MAUS.mouse.scroll(0, 2)
     
        if system == "skroll-down":
            MAUS.mouse.scroll(0, -2)

    def do(system, force=100) -> int:

        if system == "off":
            os.system("shutdown -h")

        if system == "up":
            MAUS.mouse.move(0, -force)

        if system == "left":
            MAUS.mouse.move(-force, 0)

        if system == "right":
            MAUS.mouse.move(force, 0)

        if system == "down":
            MAUS.mouse.move(0, force)

        if system == "mouse-right":
            MAUS.mouse.press(MAUS.Button.right)
            MAUS.mouse.release(MAUS.Button.right)

        if system == "mouse-left":
            MAUS.mouse.press(MAUS.Button.left)
            MAUS.mouse.release(MAUS.Button.left)

        if system == "volume+":
            from pynput.keyboard import Key, Controller
            keyboard = Controller() #контроллер клавы
            keyboard.press(Key.media_volume_up)
            keyboard.release(Key.media_volume_up)

        if system == "volume-":
            from pynput.keyboard import Key, Controller
            keyboard = Controller() #контроллер клавы
            keyboard.press(Key.media_volume_down)
            keyboard.release(Key.media_volume_down)

        return force

class KEYBORD:
    from pynput.keyboard import Key, Controller
    keyboard = Controller() #контроллер клавы
    def write(text):
        KEYBORD.keyboard.type(text)
        KEYBORD.keyboard.press(KEYBORD.Key.enter)
        KEYBORD.keyboard.release(KEYBORD.Key.enter)

class MEDIA:
    from pynput.keyboard import Key, Controller
    keyboard = Controller() #контроллер клавы
    def do(media):

        if media == "play":
            MEDIA.keyboard.press(MEDIA.Key.space)
            MEDIA.keyboard.release(MEDIA.Key.space)
            
        if media == "full":
            MEDIA.keyboard.press('f')
            MEDIA.keyboard.release('f')
             
        if media == "c":
            MEDIA.keyboard.press('c')
            MEDIA.keyboard.release('c')
             
        if media == "mute":
            MEDIA.keyboard.press('m')
            MEDIA.keyboard.release('m')
             
        if media == "next":
            MEDIA.keyboard.press(MEDIA.Key.shift)
            MEDIA.keyboard.press('n')
            MEDIA.keyboard.release('n')
            MEDIA.keyboard.release(MEDIA.Key.shift)
             
        if media == "close":
            MEDIA.keyboard.press(MEDIA.Key.alt)
            MEDIA.keyboard.press(MEDIA.Key.f4)
            MEDIA.keyboard.release(MEDIA.Key.f4)
            MEDIA.keyboard.release(MEDIA.Key.alt)
              