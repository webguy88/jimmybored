import pyglet
from pyglet.window import key
from pyglet.window import mouse
from pyglet import resource
from pyglet import sprite
from pyglet.gl import gl
from pyglet import clock
from pyglet import text
from random import randint

# Resource-related
resource.path = ['./resources']
resource.reindex()
pyglet.options['debug_gl'] = False

room_floor = resource.image('bg.png')
dark_effect = resource.image('effect.png')
bed_img = resource.image('bed.png')
wall_img = resource.image('wall.png')
bass_body = resource.image('bass.png')
bass_neck = resource.image('bass_neck.png')
bass_outline = resource.image('bass_outline.png')
bed_outline = resource.image('bed_outline.png')
trash_can = resource.image('trash_can.png')
trash_outline = resource.image('trash_outline.png')
desk = resource.image('desk.png')
desk_outline = resource.image('desk_outline.png')
desk_game = resource.image('desk_game.png')
game_disc = resource.image('game_disc.png')
message_show = resource.image('message_show.png')
popup_button_U = resource.image('popup_button_U.png')
popup_button_S = resource.image('popup_button_S.png')

low_E = resource.media('bass_low_E.wav', streaming=False)
low_F = resource.media('bass_low_F.wav', streaming=False)
low_G = resource.media('bass_low_G.wav', streaming=False)
low_A = resource.media('bass_low_A.wav', streaming=False)
low_B = resource.media('bass_low_B.wav', streaming=False)
low_C = resource.media('bass_low_C.wav', streaming=False)
low_D = resource.media('bass_low_D.wav', streaming=False)
high_E = resource.media('bass_high_E.wav', streaming=False)
high_F = resource.media('bass_high_F.wav', streaming=False)
high_G = resource.media('bass_high_G.wav', streaming=False)
high_A = resource.media('bass_high_A.wav', streaming=False)
high_B = resource.media('bass_high_B.wav', streaming=False)
high_C = resource.media('bass_high_C.wav', streaming=False)


bass_notes = [
    low_E,
    low_F,
    low_G,
    low_A,
    low_B,
    low_C,
    low_D,
    high_E,
    high_F,
    high_G,
    high_A,
    high_B,
    high_C,
]

# Window stuff
SCREENW = 640
SCREENH = 480
FULLSCREEN = False

window = pyglet.window.Window(SCREENW, SCREENH, caption="Jimmy is bored",
                              fullscreen=FULLSCREEN)

default_cur = window.get_system_mouse_cursor(window.CURSOR_DEFAULT)
choose_cur = window.get_system_mouse_cursor(window.CURSOR_HAND)

icon16 = resource.image('icon16.png')
icon32 = resource.image('icon32.png')
window.set_icon(icon16, icon32)

# ~~~~~~

def center_image(image):
    image.anchor_x = image.width / 2
    image.anchor_y = image.height / 2


center_image(bed_img)
center_image(wall_img)
center_image(bass_body)
center_image(bass_neck)
center_image(bass_outline)
center_image(bed_outline)
center_image(trash_can)
center_image(trash_outline)
center_image(desk)
center_image(desk_outline)
center_image(desk_game)
center_image(game_disc)
center_image(popup_button_U)
center_image(popup_button_S)

GAME = "game"
MSG = "message"

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

    def collides(self, r2):

        # Check the edge collision
        if self.x < r2.x + r2.width and \
           self.x + self.width > r2.x and \
           self.y < r2.y + r2.height and \
           self.height + self.y > r2.y:
            return True
        
        # If not in the edge collision
        return False


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
        self.y = 148
        self.vx = 0
        self.vy = 0
        self.direction = 1
        self.walking = False
        self.jimmy_idle = sprite.Sprite(self.images_idle[0])
        self.jimmy_walk_r = sprite.Sprite(self.jimmy_right)
        self.jimmy_walk_l = sprite.Sprite(self.jimmy_left)
        self.jimmy_sprite = self.jimmy_walk_r
        self.hitbox = Region(self.x, self.y, 40, 70)
        self.is_over_bass = False
        self.is_over_bed = False
        self.is_over_trash = False
        self.is_over_desktop = False
        self.has_game = False

    def draw(self):
        self.jimmy_sprite.draw()

    def detect_collision(self, hitbox):
        # Check if there's no collision between objects
        for obj in engine.current_screen.obj_list:
            if obj.solid and hitbox.collides(obj.hitbox):
                return obj

    def update(self, dt):
        new_x = self.x + self.vx * dt
        new_y = self.y + self.vy * dt
        new_hitbox = Region(new_x - 40 // 2,
                            new_y - 70 // 2,
                            width=40,
                            height=40)
        obj_hit = self.detect_collision(new_hitbox)

        if obj_hit != None:
            self.vx = 0
            self.vy = 0
            self.jimmy_sprite = self.jimmy_idle
            self.jimmy_sprite.x = self.x
            self.jimmy_sprite.y = self.y
            return

        # Calculate Jimmy sprite
        if not self.walking:
            self.jimmy_sprite = self.jimmy_idle

        if self.walking and self.direction == 0:
            self.jimmy_sprite = self.jimmy_walk_r

        elif self.walking and self.direction == 1:
            self.jimmy_sprite = self.jimmy_walk_l

        self.x = new_x
        self.y = new_y  # It's physics time :P
        self.jimmy_sprite.x = self.x
        self.jimmy_sprite.y = self.y

        # Update region
        self.hitbox = new_hitbox

    def change_direction(self, direction, vx, vy):

        # Update player state
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
        window.set_mouse_cursor(default_cur)
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


class SceneObject():
    def __init__(self, id, solid, name, x, y, width=0, height=0, sprite=None, visible=True):
        self.id = id
        self.solid = solid
        self.name = name
        self.sprite = sprite
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.visible = visible

        if sprite != None:
            self.sprite.x = self.x
            self.sprite.y = self.y

        if sprite != None and width == 0 and height == 0:
            self.hitbox = Region(self.x - self.sprite.width // 2,
                                 self.y - self.sprite.height // 2,
                                 self.sprite.width,
                                 self.sprite.height)

        else:
            self.hitbox = Region(self.x - self.width // 2,
                                 self.y - self.height // 2,
                                 self.width,
                                 self.height)


class Bedroom(Screen):

    floor = sprite.Sprite(room_floor, x=0, y=0)
    effect = sprite.Sprite(dark_effect, x=0, y=0)
    bed_spr = sprite.Sprite(bed_img, x=0, y=0)
    wall_spr = sprite.Sprite(wall_img, x=0, y=0)
    b_body_spr = sprite.Sprite(bass_body, x=0, y=0)
    b_neck_spr = sprite.Sprite(bass_neck, x=260, y=322)
    b_outline = sprite.Sprite(bass_outline, x=0, y=0)
    bd_outline = sprite.Sprite(bed_outline, x=0, y=0)
    trash = sprite.Sprite(trash_can, x=0, y=0)
    tr_outline = sprite.Sprite(trash_outline, x=0, y=0)
    desk_spr = sprite.Sprite(desk, x=0, y=0)
    desk_out = sprite.Sprite(desk_outline, x=0, y=0)
    desk_w_game = sprite.Sprite(desk_game, x=0, y=0)
    disc = sprite.Sprite(game_disc, x=600, y=435)
    popup = sprite.Sprite(message_show, x=0, y=0)
    popup_button_un = sprite.Sprite(popup_button_U, x=320, y=100)
    popup_button_se = sprite.Sprite(popup_button_S, x=320, y=100)

    def __init__(self):
        self.obj_list = []
        self.layer = GAME
        self.mouse_over_button = False
        self.popup_button_region = Region(self.popup_button_un.x - self.popup_button_un.width // 2,
                                          self.popup_button_un.y - self.popup_button_un.height // 2,
                                          234, 84)

        # Texts
        self.bed_text = text.Label(
            """
                   That bed looks comfy, 
            but you don't feel like sleeping
            """
                                   , x=280, y=160,
                                   anchor_x='center', anchor_y='center',
                                   font_size=24, color=(255, 255, 255, 255),
                                   multiline=True, width=562, height=357)

        self.trash_text1 = text.Label(
            """
            You look deep into the trash...
                    You found a game!
            """, x=280, y=160,
                 anchor_x='center', anchor_y='center',
                 font_size=24, color=(255, 255, 255, 255),
                 multiline=True, width=562, height=357
        )

        self.trash_text2 = text.Label(
            """
             You already looked in here...
            """, x=280, y=160,
                 anchor_x='center', anchor_y='center',
                 font_size=24, color=(255, 255, 255, 255),
                 multiline=True, width=562, height=357
        )

        self.game_text1 = text.Label(
            """
             Seems like the perfect spot
                         for a game...

            """, x=280, y=140,
                 anchor_x='center', anchor_y='center',
                 font_size=24, color=(255, 255, 255, 255),
                 multiline=True, width=562, height=357
        )

        self.game_text2 = text.Label(
            """
            Looks like you have a game!
              Do you want to play it?
            """, x=280, y=140,
                 anchor_x='center', anchor_y='center',
                 font_size=24, color=(255, 255, 255, 255),
                 multiline=True, width=562, height=357
        )

        self.message = None

    def draw(self):
        self.floor.draw()

        for obj in self.obj_list:
            if obj.sprite != None and obj.visible:
                obj.sprite.draw()

        player.draw()
        self.b_neck_spr.draw()
        self.effect.draw()

        if player.has_game:
            self.disc.draw()

        if self.layer == MSG:
            self.popup.draw()
            self.message.draw()

            if self.mouse_over_button:
                self.popup_button_se.draw()
            else:
                self.popup_button_un.draw()

        # Debugging
        ...

    def on_click(self, x, y, button):
        if self.layer == MSG:
            
            if self.popup_button_region.contain(x, y):
                self.layer = GAME

            if self.popup_button_region.contain(x, y) and \
               self.message == self.trash_text1:
                self.layer = GAME
                player.has_game = True

            if self.popup_button_region.contain(x, y) and \
               self.message == self.game_text2:
                engine.set_current_screen(fishing_game)

    def on_key_press(self, symbol, modifiers):
        if self.layer == GAME:
            if player.is_over_bass and symbol == key.SPACE:
                bass_notes[randint(0, 12)].play()

            if player.is_over_bed and symbol == key.SPACE:
                self.layer = MSG
                self.message = self.bed_text

            if player.is_over_trash and symbol == key.SPACE \
               and not player.has_game:
                self.layer = MSG
                self.message = self.trash_text1

            elif player.is_over_trash and symbol == key.SPACE \
                 and player.has_game:
                self.layer = MSG
                self.message = self.trash_text2

            if player.is_over_desktop and symbol == key.SPACE \
               and not player.has_game:
                 self.layer = MSG
                 self.message = self.game_text1

            if player.is_over_desktop and symbol == key.SPACE \
               and player.has_game:
                 self.layer = MSG
                 self.message = self.game_text2

    def update(self, dt):

        # PLAYER MOVEMENT & BEHAVIOUR

        if self.layer == GAME:

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

            # Outlining
            if player.hitbox.collides(outline_bass.hitbox):
                outline_bass.visible = True
                player.is_over_bass = True
            else:
                outline_bass.visible = False
                player.is_over_bass = False

            if player.hitbox.collides(outline_bed.hitbox):
                outline_bed.visible = True
                player.is_over_bed = True
            else:
                outline_bed.visible = False
                player.is_over_bed = False

            if player.hitbox.collides(outline_trash.hitbox):
                outline_trash.visible = True
                player.is_over_trash = True
            else:
                outline_trash.visible = False
                player.is_over_trash = False

            if player.hitbox.collides(outline_desktop.hitbox):
                outline_desktop.visible = True
                player.is_over_desktop = True
            else:
                outline_desktop.visible = False
                player.is_over_desktop = False
            
        # ~~~~~~~~~~~~~~

        # POPUPS RELATED
        elif self.layer == MSG:
    
            if self.popup_button_region.contain(engine.mouse_X, engine.mouse_Y):
                self.mouse_over_button = True
                window.set_mouse_cursor(choose_cur)
            else:
                self.mouse_over_button = False

    def is_key_pressed(self):
        for _k, v in keys.items():
            if v:
                return True
        
        return False


# ~~~~~~~~~


class FishingGame(Screen):
    def __init__(self):
        self.obj_list = []

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
player = Player()

# Bedroom objects
wall = SceneObject(id=0, solid=True, name="wall", x=320, y=372, sprite=Bedroom.wall_spr)
bed = SceneObject(id=1, solid=True, name="bed", x=80, y=240, sprite=Bedroom.bed_spr)
boundary_down = SceneObject(id=2, solid=True, name="b_bottom", x=320, y=0, width=SCREENW, height=1)
boundary_left = SceneObject(id=3, solid=True, name="b_left", x=0, y=0, width=1, height=SCREENH)
boundary_right = SceneObject(id=4, solid=True, name="b_right", x=639, y=0, width=1, height=SCREENH)
body_bass = SceneObject(id=5, solid=True, name="bass_body", x=260, y=235, sprite=Bedroom.b_body_spr)
outline_bass = SceneObject(id=6, solid=False, name="bass_outline", x=260, y=285, width=87, height=205, sprite=Bedroom.b_outline, visible=False)
outline_bed = SceneObject(id=7, solid=False, name="bed_outline", x=80, y=240, sprite=Bedroom.bd_outline, visible=False)
trash = SceneObject(id=8, solid=True, name="trash_can", x=580, y=50, sprite=Bedroom.trash)
outline_trash = SceneObject(id=9, solid=False, name="trash_outline", x=580, y=50, width=80, height=80, sprite=Bedroom.tr_outline, visible=False)
desktop = SceneObject(id=10, solid=True, name="desktop", x=480, y=255, sprite=Bedroom.desk_spr)
outline_desktop = SceneObject(id=11, solid=False, name="desktop_outline", x=480, y=255, width=190, height=125, sprite=Bedroom.desk_out, visible=False)

# Fishing game objects
...

bedroom = Bedroom()
fishing_game = FishingGame()

# Add all the scene objects
bedroom.obj_list.append(wall)
bedroom.obj_list.append(outline_bed)
bedroom.obj_list.append(bed)
bedroom.obj_list.append(boundary_down)
bedroom.obj_list.append(boundary_left)
bedroom.obj_list.append(boundary_right)
bedroom.obj_list.append(outline_bass)
bedroom.obj_list.append(body_bass)
bedroom.obj_list.append(outline_trash)
bedroom.obj_list.append(trash)
bedroom.obj_list.append(outline_desktop)
bedroom.obj_list.append(desktop)

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
