import pyglet as pg
import math

def reg_generator(gen, when_end=None):
    next(gen)
    def helper(dt):
        try:
            gen.send(dt)
            # next(gen)
        except StopIteration:
            pg.clock.unschedule(helper)
            if when_end:
                when_end()
    pg.clock.schedule(helper)

def tween_x(interval, item, func, start, end):
    time = 0
    item.x = start
    while time < interval:
        time += yield
        item.x = start + func(time/interval) * (end - start)
    item.x = end

def load_sprite(img_file, batch):
    return center_screen(pg.sprite.Sprite(center_anchor(pg.image.load(img_file)), batch=batch))

def center_screen(spr):
    spr.x = window.width / 2
    spr.y = window.height / 2
    return spr

def center_anchor(thing):
    global window
    thing.anchor_x = thing.width // 2
    thing.anchor_y = thing.height // 2
    return thing

def init(win):
    global START_X, END_X

    global window, spr_text, spr_overlay, spr_mask, flag_opening, timer, batch
    window = win
    
    START_X = window.width * -0.4
    END_X = window.width * 1.4

    batch = pg.graphics.Batch()
    spr_overlay = load_sprite('img_overlay.png', batch=batch)
    spr_text = load_sprite('img_text.png', batch=batch)
    spr_mask = load_sprite('img_mask.png', batch=batch)
    flag_opening = False
    # @window.event
    # def on_mouse_motion(x, y, dx, dy):
    #     spr_overlay.x = x
    #     spr_mask.x = x

def update(dt):
    spr_mask.x = spr_overlay.x

def moving_out(dt):
    global flag_opening
    flag_opening = False

ease_func0 = lambda x:1-math.cos(math.pi*x/2)**3
ease_func1 = lambda x:math.cos(math.pi*(1-x)/2)**3

def wait_0(*args):
    reg_generator(tween_x(0.6, spr_text, ease_func0, START_X, window.width/2))
def wait_1(*args):
    def when_end():
        global flag_opening
        flag_opening = False
    reg_generator(tween_x(0.6, spr_overlay, ease_func1, window.width/2, END_X), when_end)

def close_helper(*args):
    reg_generator(tween_x(0.6, spr_text, ease_func1, window.width/2, END_X))
    pg.clock.schedule_once(wait_1, 0.05)

def open():
    pg.clock.unschedule(close_helper)
    global flag_opening
    flag_opening = True
    reg_generator(tween_x(0.6, spr_overlay, ease_func0, START_X, window.width/2))
    pg.clock.schedule_once(wait_0, 0.1)

def close():
    pg.clock.schedule_once(close_helper, 0.4)

def draw():
    if flag_opening:
        batch.draw()
