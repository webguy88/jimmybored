import pyglet
from pyglet.window import key
from pyglet.window import mouse
from pyglet import resource
from pyglet import sprite
from pyglet.gl import gl

# Change current path
resource.path = ['./resources']
resource.reindex()

SCREENW = 800
SCREENH = 600
FULLSCREEN = False

window = pyglet.window.Window(SCREENW, SCREENH, caption="Jimmy is bored",
                              fullscreen=FULLSCREEN)

default_cur = window.get_system_cursor(window.CURSOR_DEFAULT)
choose_cur = window.get_system_cursor(window.CURSOR_HAND)


def center_image(image):
    image.anchor_x = image.width / 2
    image.anchor_y = image.height / 2


def center_image_list(image):
    for img in image:
        img.anchor_x = image.width / 2
        img.anchor_y = image.height / 2


class Player():
    def __init__(self):
        pass

        self.x = 0
        self.y = 0
        self.vx = 0
        self.vy = 0
        self.direction = 1

    def draw(self):
        pass

    def update(self, dt):
        self.x = self.x + self.vx * dt
        self.y = self.y + self.vy * dt  # It's physics time :P

    def change_direction(self, direction, vx, vy):
        self.direction = direction
        self.vx = vx
        self.vy = vy


class Engine():
    def __init__(self, current_screen):
        self.mouse_X = 0
        self.mouse_Y = 0
        self.current_screen = current_screen

    def draw(self):
        self.current_screen.draw()

    def on_click(self, x, y, button):
        self.current_screen.on_click(x, y, button)

    def mouse_XY(self, x, y, dx, dy):
        self.mouse_X = x
        self.mouse_Y = y

    def on_key_press(self, symbol, modifiers):
        self.current_screen.on_key_press(symbol, modifiers)

    def update(self, dt):
        self.current_screen.update(dt)

    def set_current_screen(self, current_screen):
        self.current_screen = current_screen


class Screen():
    def __init__(self):
        pass

    def draw(self):
        pass

    def on_click(self, x, y, button):
        pass

    def on_key_press(self, symbol, modifiers):
        pass

    def update(self, dt):
        pass


# Instances of classes
# Screens go first

engine = Engine(None)


@window.event
def on_draw():
    window.clear()
    engine.draw()


@window.event
def on_mouse_press(x, y, button):
    if button == mouse.LEFT:
        engine.on_click(x, y, button)


@window.event
def on_mouse_motion(x, y, dx, dy):
    engine.mouse_XY(x, y, dx, dy)
    pass


@window.event
def on_key_press(symbol, modifiers):
    engine.on_key_press(symbol, modifiers)


@window.event
def update(dt):
    engine.update(dt)


pyglet.app.run()
