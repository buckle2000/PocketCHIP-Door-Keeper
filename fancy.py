import pyglet as pg

def reg_generator(gen):
    next(gen)
    def helper(dt):
        try:
            gen.send(dt)
            # next(gen)
        except StopIteration:
            pg.clock.unschedule(helper)
    pg.clock.schedule(helper)

def tween_x(interval, item, func, start, end):
    time = 0
    item.x = start
    while time < interval:
        time += yield
        item.x = start + func(time/interval) * (end - start)
    item.x = end

def load_sprite(img_file):
    return center_screen(pg.sprite.Sprite(center_anchor(pg.image.load(img_file))))

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

    global window, spr_text, spr_overlay, spr_mask, flag_opening, timer
    window = win
    
    START_X = window.width * -0.4
    END_X = window.width * 1.4

    spr_text = load_sprite('img_text.png')
    spr_overlay = load_sprite('img_overlay.png')
    spr_mask = load_sprite('img_mask.png')
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

def open():
    global flag_opening
    flag_opening = True
    spr_overlay.x = START_X
    reg_generator(tween_x(0.3, spr_overlay, lambda x:x*x, START_X, window.width/2))

def close():
    global flag_opening
    reg_generator(tween_x(0.3, spr_overlay, lambda x:1-(1-x)*(1-x), window.width/2, END_X))

def draw():
    if flag_opening:
        spr_overlay.draw()
        spr_text.draw()
        spr_mask.draw()
