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

window = pg.window.Window(fullscreen=True)

resolution_str = str(window.width)+'x'+str(window.height)
print("Resolution:", resolution_str)
resolution_label = pg.text.Label(resolution_str)

@window.event
def on_draw():
    window.clear()
    resolution_label.draw()


def update(dt):
    pass


def update_GPIO(dt):
    pass  # TODO


def update_network(dt):
    pass  # TODO

pg.clock.schedule(update)
pg.app.run()
