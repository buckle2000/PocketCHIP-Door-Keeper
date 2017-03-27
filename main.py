#import os,sys
import pyglet as pg
import CHIP_IO.GPIO as GPIO
import requests

window = pg.window.Window()

@window.event
def on_draw():
  window.clear()

def update():
  pass # TODO

def update_GPIO():
  pass # TODO

def update_network():
  pass # TODO

pg.clock.schedule(update)
pg.app.run()

