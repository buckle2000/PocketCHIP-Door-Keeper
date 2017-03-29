import sys
import atexit
import pyglet as pg
from requests_futures.sessions import FuturesSession
import fancy as fancy_demo

PIN_BUTTON = "GPIO3"
PIN_RELAY  = "GPIO6"
DEV = sys.platform == 'win32'

cooldown = 0.

if DEV:
    try:
        import IPython
    except:
        pass
else:
    import CHIP_IO.GPIO as GPIO

def atexit_callback():
    if not DEV:
        GPIO.cleanup()
atexit.register(atexit_callback)

if not DEV:
    GPIO.setup(PIN_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(PIN_RELAY, GPIO.OUT)
    print("Init GPIO")

# IPython.embed()

requests_session = FuturesSession()

if DEV:
    window = pg.window.Window(width=480, height=272) # simlulate pocketCHIP
else:
    window = pg.window.Window(fullscreen=True)

str_resolution = str(window.width)+'x'+str(window.height)
label_resolution = pg.text.Label(str_resolution)
print("Resolution:", str_resolution)
print("PIN_BUTTON:", PIN_BUTTON)
print("PIN_RELAY:", PIN_RELAY)

label_info = pg.text.Label('Loading')
label_info.width = window.width
label_info.multiline = True
label_info.y = window.height - label_info.content_height

str_format = "Door: {door}\nNetwork: {network}\nCD: {cooldown:.1f}"
if not DEV:
    str_format += "\nButton down: {btndown}"

str_door = "Closing"
str_network = "Connecting..."

@window.event
def on_draw():
    window.clear()
    fancy_demo.draw()
    label_info.draw()
    label_resolution.draw()

def update(dt):
    global cooldown
    cooldown -= dt
    if cooldown < 0.:
        cooldown = 0.
    str_btndown = "No"
    if not DEV and not GPIO.input(PIN_BUTTON):
        str_btndown = "Yes"
    label_info.text = str_format.format(door=str_door, network=str_network, btndown=str_btndown, cooldown=cooldown)
    fancy_demo.update(dt)

def network_callback(sess,resp):
    global str_network
    str_network = str(resp.status_code)
    if resp.status_code == 404:
        pg.clock.schedule_once(update_network, 1.)
        return
    elif resp.status_code == 200:
        open_sesame()
    elif resp.status_code == 204:
        pass # do nothing
    else:
        str_network = str(resp.status_code)
        return
    pg.clock.schedule_once(update_network, 1.)

def update_network(dt):
    requests_session.get('http://pacific-harbor-49025.herokuapp.com/delete/arduino', background_callback=network_callback)

def open_sesame(*args):
    global cooldown
    if cooldown == 0.:
        cooldown = 3
    else:
        return
    global str_door
    pg.clock.unschedule(close_sesame)
    if not DEV:
        GPIO.output(PIN_RELAY, GPIO.HIGH)
    if str_door != "opening":
        str_door = "opening"
        fancy_demo.open()
    pg.clock.schedule_once(close_sesame, 1.) # supply current for 1s
    
def close_sesame(*args):
    global str_door
    str_door = "closing"
    if not DEV:
        GPIO.output(PIN_RELAY, GPIO.LOW)
    fancy_demo.close()

@window.event
def on_key_press(symbol, modifiers):
    if symbol == pg.window.key.O:
        open_sesame()

@window.event
def on_mouse_press(x, y, button, modifiers):
    open_sesame()

pg.clock.set_fps_limit(60)
pg.clock.schedule(update)
pg.clock.schedule_once(update_network, 0.)
if not DEV:
    GPIO.add_event_detect(PIN_BUTTON, GPIO.FALLING, open_sesame)

fancy_demo.init(window)

pg.app.run()
