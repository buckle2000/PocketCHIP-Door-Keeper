import sys
import requests
import pyglet as pg

DEV = sys.platform == 'win32'

if DEV:
    try:
        import IPython
    except:
        pass
else:
    import CHIP_IO.GPIO as GPIO
    GPIO.setup("GPIO3", GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup("GPIO6", GPIO.OUT)
# IPython.embed()

window = pg.window.Window(fullscreen=True)

str_resolution = str(window.width)+'x'+str(window.height)
label_resolution = pg.text.Label(str_resolution)
print("Resolution:", str_resolution)

label_info = pg.text.Label('Loading')
label_info.width = window.width
label_info.multiline = True
label_info.y = window.height - label_info.content_height

str_format = "Door: {door}\nNetwork: {network}"
if not DEV:
    str_format += "\nButton down: {btndown}"

str_door = "Closing"
str_network = "Connecting..."

@window.event
def on_draw():
    window.clear()
    label_info.draw()
    label_resolution.draw()

def update(dt):
    str_btndown = "No"
    if not DEV and not GPIO.input("GPIO3"):
        str_btndown = "Yes"
    label_info.text = str_format.format(door=str_door, network=str_network, btndown=str_btndown)

def update_network(dt):
    pass  # TODO

def open_sesame(*args):
    global str_door
    pg.clock.unschedule(close_sesame)
    if not DEV:
        GPIO.output("GPIO6", GPIO.HIGH)
    str_door = "opening"
    pg.clock.schedule(close_sesame, 1.) # supply current for 1s
    
def close_sesame():
    global str_door
    str_door = "closing"
    if not DEV:
        GPIO.output("GPIO6", GPIO.LOW)

pg.clock.set_fps_limit(60)
pg.clock.schedule(update)
pg.clock.schedule_interval(update_network, 1.)
if not DEV:
    GPIO.add_event_detect("GPIO3", GPIO.FALLING, open_sesame)

pg.app.run()

if not DEV:
    GPIO.cleanup()
