import pyglet
from pyglet.window import key
from pyglet.window import mouse
from pyglet import resource
from pyglet import sprite
from pyglet.gl import gl
from pyglet import clock

# Resource-related
resource.path = ['./resources']
resource.reindex()
pyglet.options['debug_gl'] = False

room_floor = resource.image('bg.png')
dark_effect = resource.image('effect.png')

# Window stuff
SCREENW = 640
SCREENH = 480
FULLSCREEN = False

window = pyglet.window.Window(SCREENW, SCREENH, caption="Jimmy is bored",
                              fullscreen=FULLSCREEN)

default_cur = window.get_system_mouse_cursor(window.CURSOR_DEFAULT)
choose_cur = window.get_system_mouse_cursor(window.CURSOR_HAND)

icon16 = None
icon32 = None

# ~~~~~~

def center_image(image):
    image.anchor_x = image.width / 2
    image.anchor_y = image.height / 2


# GL stuff
gl.glEnable(gl.GL_BLEND)
gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)


class Rect:

    def __init__(self, x, y, w, h):
        self.set(x, y, w, h)

    def draw(self):
        pyglet.graphics.draw(4, gl.GL_QUADS, self._quad)

    def set(self, x=None, y=None, w=None, h=None):
        self._x = self._x if x is None else x
        self._y = self._y if y is None else y
        self._w = self._w if w is None else w
        self._h = self._h if h is None else h
        self._quad = ('v2f', (self._x, self._y,
                              self._x + self._w, self._y,
                              self._x + self._w, self._y + self._h,
                              self._x, self._y + self._h))

    def __repr__(self):
        return f"Rect(x={self._x}, y={self._y}, w={self._w}, h={self._h})"


# Allows clicks in certain areas
class Region(object):

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def contain(self, x, y):
        inside_x = False
        inside_y = False

        if x >= self.x and x <= (self.x + self.width):
            inside_x = True

        if y >= self.y and y <= (self.y + self.height):
            inside_y = True

        if inside_x and inside_y:
            return True
        else:
            return False

    def draw(self):
        r = Rect(self.x, self.y, self.width, self.height)
        r.draw()


# ~~~~~~~~~~~~~~~~~

# Gameplay stuff
class Player():

    images_idle = [
        resource.image('playerR.png'),
        resource.image('playerL.png')
    ]

    images_walking_r = [
        resource.image('playerR_walk1.png'),
        resource.image('playerR.png'),
        resource.image('playerR_walk2.png')
    ]

    images_walking_l = [
        resource.image('playerL_walk1.png'),
        resource.image('playerL.png'),
        resource.image('playerL_walk2.png')
    ]

    jimmy_right = pyglet.image.Animation.from_image_sequence(images_walking_r, duration=0.1, loop=True)
    jimmy_left = pyglet.image.Animation.from_image_sequence(images_walking_l, duration=0.1, loop=True)

    def __init__(self):
        for img in self.images_idle:
            img.anchor_x = img.width / 2
            img.anchor_y = img.height / 2

        for img in self.images_walking_r:
            img.anchor_x = img.width / 2
            img.anchor_y = img.width / 2

        for img in self.images_walking_l:
            img.anchor_x = img.width / 2
            img.anchor_y = img.width / 2

        self.x = 320
        self.y = 240
        self.vx = 0
        self.vy = 0
        self.direction = 1
        self.walking = False
        self.jimmy_idle = sprite.Sprite(self.images_idle[0])
        self.jimmy_walk_r = sprite.Sprite(self.jimmy_right)
        self.jimmy_walk_l = sprite.Sprite(self.jimmy_left)
        self.jimmy_sprite = self.jimmy_walk_r
        self.player_hitbox = Region(self.x, self.y, 40, 70)

    def draw(self):
        self.jimmy_sprite.draw()

    def update(self, dt):
        self.x = self.x + self.vx * dt
        self.y = self.y + self.vy * dt  # It's physics time :P
        self.jimmy_idle.x = self.x
        self.jimmy_idle.y = self.y
        self.jimmy_walk_r.x = self.jimmy_idle.x
        self.jimmy_walk_r.y = self.jimmy_idle.y
        self.jimmy_walk_l.x = self.jimmy_idle.x
        self.jimmy_walk_l.y = self.jimmy_idle.y

        # Update region
        self.player_hitbox.x = (self.jimmy_idle.x - 20)
        self.player_hitbox.y = (self.jimmy_idle.y - 35)

        # Calculate Jimmy sprite
        if not self.walking:
            self.jimmy_sprite = self.jimmy_idle
        
        if self.walking and self.direction == 0:
            self.jimmy_sprite = self.jimmy_walk_r

        elif self.walking and self.direction == 1:
            self.jimmy_sprite = self.jimmy_walk_l

    def change_direction(self, direction, vx, vy):
        self.direction = direction
        self.vx = vx
        self.vy = vy
        self.jimmy_idle.image = self.images_idle[self.direction]


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


class Bedroom(Screen):

    floor = sprite.Sprite(room_floor, x=0, y=0)
    effect = sprite.Sprite(dark_effect, x=0, y=0)

    def __init__(self):
        pass

    def draw(self):
        self.floor.draw()
        player.draw()
        self.effect.draw()

        # Debugging
        ...

    def on_click(self, x, y, button):
        pass

    def on_key_press(self, symbol, modifiers):
        pass

    def update(self, dt):

        # PLAYER MOVEMENT & BEHAVIOUR

        # Normal movement
        if keys[key.W]:
            player.change_direction(0, 0, 170)
            player.walking = True

        if keys[key.A]:
            player.change_direction(1, -170, 0)
            player.walking = True

        if keys[key.S]:
            player.change_direction(1, 0, -170)
            player.walking = True

        if keys[key.D]:
            player.change_direction(0, 170, 0)
            player.walking = True

        # Diagonal implementation
        if keys[key.W] and keys[key.A]:
            player.change_direction(1, -160, 160)
            player.walking = True

        if keys[key.W] and keys[key.D]:
            player.change_direction(0, 160, 160)
            player.walking = True

        if keys[key.S] and keys[key.A]:
            player.change_direction(1, -160, -160)
            player.walking = True
        
        if keys[key.S] and keys[key.D]:
            player.change_direction(0, 160, -160)
            player.walking = True

        # Cancel two keys at the same time
        if keys[key.W] and keys[key.S]:
            player.change_direction(player.direction, 0, 0)
            player.walking = False

        if keys[key.A] and keys[key.D]:
            player.change_direction(player.direction, 0, 0)
            player.walking = False

        if not self.is_key_pressed():
            player.change_direction(player.direction, 0, 0)
            player.walking = False

        # Collision
        ...

        # ~~~~~~~~~~~~~~

    def is_key_pressed(self):
        for _k, v in keys.items():
            if v:
                return True
        
        return False


# ~~~~~~~~~


# Instances of classes
# Screens go first
player = Player()
bedroom = Bedroom()
engine = Engine(bedroom)


@window.event
def on_draw():
    window.clear()
    engine.draw()


@window.event
def on_mouse_press(x, y, button, modifiers):
    if button & mouse.LEFT:
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
    player.update(dt)


keys = key.KeyStateHandler()
window.push_handlers(keys)

clock.schedule_interval(update, 1/30)
pyglet.app.run()
