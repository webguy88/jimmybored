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
resource.path = ['../resources']
resource.reindex()
pyglet.options['debug_gl'] = False

dark = resource.image('black.png')
playground_floor = resource.image('bg.png')
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
fish_disc = resource.image('fish_disc.png')
game_bag = resource.image('game_bag.png')
message_show = resource.image('message_show.png')
close_window = resource.image('close_window.png')
popup_button_U = resource.image('popup_button_U.png')
popup_button_S = resource.image('popup_button_S.png')

hall1 = resource.image('up_hall.png')

menu_screen = resource.image('main_menu.png')
menu_dark = resource.image('menu_dark.png')
logo = resource.image('logo.png')
button_play = resource.image('button_play.png')
info = resource.image('info.png')

credits_back = resource.image('credits_back.png')
pageL = resource.image('pageL.png')
pageR = resource.image('pageR.png')
controls_screen = resource.image('controls_screen.png')

fisher_menu = resource.image('fisher_menu.png')
fisher_background = resource.image('fisher_background.png')
fisher_sea = resource.image('fisher_sea.png')
fish = resource.image('fish.png')
fisher_won = resource.image('fisher_won.png')
fisher_lost = resource.image('fisher_lost.png')
tv_effect = resource.image('tv_effect.png')

stamina_meter = resource.image('stamina_meter.png')
stamina0 = resource.image('stamina0.png')
stamina1 = resource.image('stamina1.png')
stamina2 = resource.image('stamina2.png')
stamina3 = resource.image('stamina3.png')
stamina4 = resource.image('stamina4.png')

black = sprite.Sprite(dark, x=0, y=0)

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
select = resource.media('select.wav', streaming=False)
fisher_begin = resource.media('fisher_begin.wav', streaming=False)
got_fish = resource.media('got_fish.wav', streaming=False)
fisher_lose = resource.media('fisher_lost.wav', streaming=False)
fisher_win = resource.media('fisher_win.wav', streaming=False)

bg_music = resource.media('bg_music.wav', streaming=False)
fisher_music = resource.media('fisher_music.wav', streaming=False)

# Looping music
main_music = pyglet.media.Player()
main_music.queue(bg_music)
main_music.loop = True

fish_music = pyglet.media.Player()
fish_music.queue(fisher_music)
fish_music.loop = True

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
RESIZE = True

window = pyglet.window.Window(SCREENW, SCREENH, caption="Jimmy is bored",
                              fullscreen=FULLSCREEN, resizable=RESIZE)
target_resolution = 640, 480

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
center_image(fish_disc)
center_image(popup_button_U)
center_image(popup_button_S)
center_image(close_window)

center_image(logo)
center_image(button_play)
center_image(info)

center_image(credits_back)
center_image(fish)

SPLASH = "splash"
MENU = "menu"
GAME = "game"
FISHING = "fishing"
MSG = "message"

# GL stuff
gl.glEnable(gl.GL_BLEND)
gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)


class FixedResolution:
    def __init__(self, window, width, height, filtered=False):
        self.window = window
        self.width = width
        self.height = height
        self.filtered = filtered
        self._viewport = 0, 0, 0, 0, 0
        self._calculate_viewport(self.window.width, self.window.height)
        self.cam_x = 0
        self.cam_y = 0

        self.texture = pyglet.image.Texture.create(width, height,
                                                   rectangle=True)

        if not filtered:
            pyglet.image.Texture.default_min_filter = gl.GL_NEAREST
            pyglet.image.Texture.default_mag_filter = gl.GL_NEAREST
            gl.glTexParameteri(self.texture.target, gl.GL_TEXTURE_MAG_FILTER,
                               gl.GL_NEAREST)
            gl.glTexParameteri(self.texture.target, gl.GL_TEXTURE_MIN_FILTER,
                               gl.GL_NEAREST)

        def on_resize(w, h):
            self._calculate_viewport(w, h)
            self.window_w, self.window_h = w, h

        self.window.on_resize = on_resize

    def _calculate_viewport(self, new_screen_width, new_screen_height):
        aspect_ratio = self.width / self.height
        aspect_width = new_screen_width
        aspect_height = aspect_width / aspect_ratio + 0.5
        if aspect_height > new_screen_height:
            aspect_height = new_screen_height
            aspect_width = aspect_height * aspect_ratio + 0.5

        if not self.filtered:
            gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER,
                               gl.GL_NEAREST)
            gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER,
                               gl.GL_NEAREST)

        self._viewport = (int((new_screen_width / 2) - (aspect_width / 2)),
                          int((new_screen_height / 2) - (aspect_height / 2)),
                          0,
                          int(aspect_width),
                          int(aspect_height))

    def __enter__(self):
        gl.glViewport(0, 0, self.width, self.height)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glOrtho(0, self.width, 0, self.height, -255, 255)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glTranslatef(self.cam_x, self.cam_y, 0)

    def set_camera(self, x=0, y=0):
        self.cam_x = -x
        self.cam_y = -y

    def __exit__(self, *unused):
        window = self.window
        buffer = pyglet.image.get_buffer_manager().get_color_buffer()
        self.texture.blit_into(buffer, 0, 0, 0)

        gl.glViewport(0, 0, window.width, window.height)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glOrtho(0, window.width, 0, window.height, -1, 1)
        gl.glMatrixMode(gl.GL_MODELVIEW)

        gl.glClearColor(0, 0, 0, 1)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        gl.glLoadIdentity()

        self.texture.blit(*self._viewport)

    def begin(self):
        self.__enter__()

    def end(self):
        self.__exit__()


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

    fisher_sprite = resource.image('fisher_sprite.png')
    fisher_grab = resource.image('fisher_sprite_grab.png')

    jimmy_right = pyglet.image.Animation.from_image_sequence(images_walking_r,
                                                             duration=0.1,
                                                             loop=True)
    jimmy_left = pyglet.image.Animation.from_image_sequence(images_walking_l,
                                                            duration=0.1,
                                                            loop=True)

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

        center_image(self.fisher_sprite)
        center_image(self.fisher_grab)

        self.x = 320
        self.y = 148
        self.vx = 0
        self.vy = 0
        self.direction = 1
        self.walking = False
        self.stamina = 5
        self.is_sleeping = False
        self.jimmy_idle = sprite.Sprite(self.images_idle[0])
        self.jimmy_walk_r = sprite.Sprite(self.jimmy_right)
        self.jimmy_walk_l = sprite.Sprite(self.jimmy_left)
        self.fisherman = sprite.Sprite(self.fisher_sprite)
        self.fisherman_grab = sprite.Sprite(self.fisher_grab)
        self.sprite = self.jimmy_walk_r
        self.hitbox = Region(self.x, self.y, 40, 70)

        self.is_over_bass = False
        self.is_over_bed = False
        self.is_over_trash = False
        self.is_over_desktop = False
        self.games = []
        self.game_selected = ""

    def draw(self):
        self.sprite.draw()

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

        if engine.current_screen == bedroom:
            if obj_hit is not None:
                self.vx = 0
                self.vy = 0
                self.sprite = self.jimmy_idle
                self.sprite.x = self.x
                self.sprite.y = self.y
                return

        elif engine.current_screen == fishing_game:
            if obj_hit is not None:
                self.vx = 0
                self.sprite = self.fisherman
                self.sprite.x = self.x
                self.sprite.y = self.y
                return

        # Calculate Jimmy sprite
        if engine.current_screen in [bedroom, hall_upper]:
            if not self.walking:
                self.sprite = self.jimmy_idle

            if self.walking and self.direction == 0:
                self.sprite = self.jimmy_walk_r

            elif self.walking and self.direction == 1:
                self.sprite = self.jimmy_walk_l

            if self.is_sleeping:
                self.x = 77
                self.y = 236
                self.sprite = self.jimmy_walk_r

        if engine.current_screen == fishing_game:
            if not fishing_game.caught_something:
                self.sprite = self.fisherman
            else:
                self.sprite = self.fisherman_grab

        self.x = new_x
        self.y = new_y  # It's physics time :P
        self.sprite.x = self.x
        self.sprite.y = self.y

        # Update region
        self.hitbox = new_hitbox

    def stamina_drain(self, dt):
        if self.stamina > 0:
            self.stamina -= 1

    def change_direction(self, direction, vx, vy):

        # Update player state
        self.direction = direction
        self.vx = vx
        self.vy = vy
        self.jimmy_idle.image = self.images_idle[self.direction]


class Fish():

    fish_right_frames = [
        resource.image('fishR_frame_1.png'),
        resource.image('fishR_frame_2.png'),
        resource.image('fishR_frame_3.png'),
        resource.image('fishR_frame_2.png')
    ]

    fishR = pyglet.image.Animation.from_image_sequence(fish_right_frames,
                                                       duration=0.1, loop=True)

    def __init__(self):
        for img in self.fish_right_frames:
            img.anchor_x = img.width // 2
            img.anchor_y = img.height // 2

        self.x = 0
        self.y = randint(50, 95)
        self.vx = 0
        self.direction = 0
        self.fish_right = sprite.Sprite(self.fishR, x=self.x, y=self.y)
        self.sprite = self.fish_right
        self.region = Region(self.sprite.x,
                             self.sprite.y,
                             self.sprite.width, self.sprite.height)

    def draw(self):
        self.sprite.draw()

    def update(self, dt):
        self.x += randint(8, 10)
        self.y += randint(-3, 3)
        self.sprite.x = self.x
        self.sprite.y = self.y
        self.region.x = self.sprite.x - self.sprite.width // 2
        self.region.y = self.sprite.y - self.sprite.height // 2

        if self.x > SCREENW + self.sprite.width:
            fishing_game.enemies.remove(self)

    def change_direction(self, direction, vx):
        self.direction = direction
        self.vx = vx


class Engine():

    def __init__(self, current_screen):
        self.began = False
        self.on_exit = False
        self.opacity = 0
        self.mouse_X = 0
        self.mouse_Y = 0
        self.current_screen = current_screen
        self.next_screen = current_screen
        self.hud = Hud()
        self.layer = SPLASH
        self.showing_games = False

        if self.layer is not MENU and \
           self.layer is not SPLASH:
            self.began = False

    def draw(self):
        self.current_screen.draw()
        self.hud.draw()
        if self.on_exit:
            self.opacity += 20
            black.opacity = min(self.opacity, 255)
            black.draw()

        elif player.is_sleeping:
            self.opacity += 5
            black.opacity = min(self.opacity, 255)
            black.draw()

    def on_click(self, x, y, button):
        x1 = int(x * SCREENW / window.width)
        y1 = int(y * SCREENH / window.height)
        self.current_screen.on_click(x1, y1, button)
        self.hud.on_click(x1, y1, button)

    def mouse_XY(self, x, y, dx, dy):
        self.mouse_X = int(x * SCREENW / window.width)
        self.mouse_Y = int(y * SCREENH / window.height)

    def on_key_press(self, symbol, modifiers):
        self.current_screen.on_key_press(symbol, modifiers)

    def update(self, dt):
        window.set_mouse_cursor(default_cur)
        self.current_screen.update(dt)
        self.hud.update(dt)

        if self.layer == GAME:
            self.showing_games = False

        if self.opacity >= 255 and \
           not player.is_sleeping:
            self.enter()

    def set_current_screen(self, current_screen):
        self.current_screen = self.next_screen

    def set_next_screen(self, next_screen):
        clock.schedule_once(self.set_current_screen, 0.2)
        self.next_screen = next_screen
        self.on_exit = True

    def enter(self):
        self.current_screen.enter()
        self.opacity = 0
        self.on_exit = False


class Hud:
    stamina_display = None
    stamina_0 = sprite.Sprite(stamina0, x=20, y=390)
    stamina_1 = sprite.Sprite(stamina1, x=20, y=390)
    stamina_2 = sprite.Sprite(stamina2, x=20, y=390)
    stamina_3 = sprite.Sprite(stamina3, x=20, y=390)
    stamina_4 = sprite.Sprite(stamina4, x=20, y=390)
    bag = sprite.Sprite(game_bag, x=565, y=405)
    popup = sprite.Sprite(message_show, x=0, y=0)
    popup_un = sprite.Sprite(popup_button_U, x=320, y=100)
    popup_se = sprite.Sprite(popup_button_S, x=320, y=100)
    close_pop = sprite.Sprite(close_window, x=581, y=108)
    disc1 = sprite.Sprite(fish_disc, x=140, y=275)

    def __init__(self):
        self.from_bag = False
        self.bag_region = Region(565, 405, 64, 64)
        self.close_region = Region(x=self.close_pop.x -
                                   self.close_pop.width // 2,
                                   y=self.close_pop.y -
                                   self.close_pop.height // 2,
                                   width=94, height=94)
        self.popup_button_region = Region(self.popup_un.x -
                                          self.popup_un.width // 2,
                                          self.popup_un.y -
                                          self.popup_un.height // 2,
                                          234, 84)

        self.disc1_region = Region(x=self.disc1.x - self.disc1.width // 2,
                                   y=self.disc1.y - self.disc1.height // 2,
                                   width=128, height=128)

    def update(self, dt):
        if player.stamina == 5:
            self.stamina_display = self.stamina_4
        if player.stamina == 4:
            self.stamina_display = self.stamina_4
        if player.stamina == 3:
            self.stamina_display = self.stamina_3
        if player.stamina == 2:
            self.stamina_display = self.stamina_2
        if player.stamina == 1:
            self.stamina_display = self.stamina_1
        if player.stamina == 0:
            self.stamina_display = self.stamina_0

        if engine.current_screen in [bedroom] and \
           self.bag_region.contain(engine.mouse_X, engine.mouse_Y) and \
           len(player.games) > 0 and not player.is_sleeping and \
           engine.layer == GAME:
            window.set_mouse_cursor(choose_cur)

        if engine.layer == MSG and \
           self.close_region.contain(engine.mouse_X, engine.mouse_Y):
            window.set_mouse_cursor(choose_cur)

        if engine.layer == MSG and \
           player.is_over_desktop and \
           not self.from_bag and \
           len(player.games) > 0 and \
           self.disc1_region.contain(engine.mouse_X, engine.mouse_Y):
            window.set_mouse_cursor(choose_cur)

    def draw(self):
        if engine.current_screen in [bedroom]:
            self.stamina_display.draw()

        if engine.current_screen in [bedroom] and \
           len(player.games) > 0:
            self.bag.draw()

        if engine.showing_games and \
           "fish" in player.games:
            self.disc1.draw()

    def on_click(self, x, y, button):
        if engine.current_screen in [bedroom] and \
           self.bag_region.contain(x, y) and \
           len(player.games) > 0 and not player.is_sleeping and \
           engine.layer == GAME:
            bedroom.message = text.Label("")
            engine.layer = MSG
            engine.showing_games = True
            self.from_bag = True

        if engine.layer == MSG and \
           not engine.showing_games and \
           self.popup_button_region.contain(x, y):
            engine.layer = GAME

        if engine.layer == MSG and \
           self.close_region.contain(x, y):
            engine.layer = GAME
            self.from_bag = False

        if engine.layer == MSG and \
           player.is_over_desktop and \
           not self.from_bag and \
           len(player.games) > 0 and \
           self.disc1_region.contain(x, y):
            engine.showing_games = False
            engine.layer = FISHING
            engine.set_next_screen(fishing_game)


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

    def enter(self):
        pass


class SceneObject():

    def __init__(self, id, solid, name, x, y, width=0, height=0, sprite=None,
                 visible=True):
        self.id = id
        self.solid = solid
        self.name = name
        self.sprite = sprite
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.visible = visible

        if sprite is not None:
            self.sprite.x = self.x
            self.sprite.y = self.y

        if sprite is not None and width == 0 and height == 0:
            self.hitbox = Region(self.x - self.sprite.width // 2,
                                 self.y - self.sprite.height // 2,
                                 self.sprite.width,
                                 self.sprite.height)

        else:
            self.hitbox = Region(self.x - self.width // 2,
                                 self.y - self.height // 2,
                                 self.width,
                                 self.height)


class SplashScreen(Screen):

    def __init__(self):
        self.obj_list = []
        self.count = 0
        self.text = text.Label("webguy88 presents...", x=320, y=240,
                               anchor_x='center', anchor_y='center',
                               font_size=24, bold=True,
                               color=(255, 255, 255, 255))

    def draw(self):
        self.text.draw()

    def update(self, dt):
        self.count += 0.5

        if self.count >= 30:
            engine.set_next_screen(main_menu)
            engine.layer = MENU


class MainMenu(Screen):

    menu = sprite.Sprite(menu_screen, x=0, y=0)
    dark = sprite.Sprite(menu_dark, x=0, y=0)
    logo_spr = sprite.Sprite(logo, x=320, y=380)
    button = sprite.Sprite(button_play, x=320, y=150)
    info_button = sprite.Sprite(info, x=35, y=35)

    def __init__(self):
        self.obj_list = []
        self.play_region = Region(self.button.x - self.button.width // 2,
                                  self.button.y - self.button.height // 2,
                                  234, 84)
        self.info_button_region = Region(self.info_button.x -
                                         self.info_button.width // 2,
                                         self.info_button.y -
                                         self.info_button.height // 2,
                                         64, 64)

        self.version_text = text.Label("v 2.0", x=608, y=40,
                                       anchor_x='center', anchor_y='center',
                                       font_size=16,
                                       color=(255, 255, 255, 255),
                                       bold=True)

        self.copyrights = text.Label("Made by webguy88 in 2020",
                                     x=495, y=15,
                                     anchor_x='center', anchor_y='center',
                                     font_size=16, color=(255, 255, 255, 255),
                                     bold=True)

    def draw(self):
        self.menu.draw()
        bedroom.b_neck_spr.draw()

        for obj in self.obj_list:
            if obj.sprite is not None and obj.visible:
                obj.sprite.draw()

        self.dark.draw()
        self.logo_spr.draw()
        self.button.draw()
        self.info_button.draw()
        self.version_text.draw()
        self.copyrights.draw()
        main_music.play()

    def on_click(self, x, y, button):
        if self.play_region.contain(x, y):
            engine.layer = GAME
            engine.set_next_screen(bedroom)
            engine.began = True

        if self.info_button_region.contain(x, y):
            engine.set_next_screen(credit_screen)

    def on_key_press(self, symbol, modifiers):
        pass

    def update(self, dt):
        if self.play_region.contain(engine.mouse_X, engine.mouse_Y):
            window.set_mouse_cursor(choose_cur)

        if self.info_button_region.contain(engine.mouse_X, engine.mouse_Y):
            window.set_mouse_cursor(choose_cur)

    def enter(self):
        pass

    def is_key_pressed(self):
        for _k, v in keys.items():
            if v:
                return True

        return False


class Credit(Screen):

    go_back = sprite.Sprite(credits_back, x=80, y=430)
    page_left = sprite.Sprite(pageL, x=240, y=5)
    page_right = sprite.Sprite(pageR, x=310, y=5)
    controls = sprite.Sprite(controls_screen, x=0, y=0)

    def __init__(self):
        self.obj_list = []
        self.back_region = Region(self.go_back.x - self.go_back.width // 2,
                                  self.go_back.y - self.go_back.height // 2,
                                  135, 86)

        self.go_left_region = Region(240, 5, 64, 64)
        self.go_right_region = Region(310, 5, 64, 64)
        self.page = 1

        # Text
        self.license = pyglet.text.Label(
            """
            Copyright (c) 2006-2008 Alex Holkner
    Copyright (c) 2008-2020 pyglet contributors
    All rights reserved.

    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions are met:

        * Redistributions of source code must retain the above copyright
            notice, this list of conditions and the following disclaimer.
        * Redistributions in binary form must reproduce the above copyright
            notice, this list of conditions and the following disclaimer in
            the documentation and/or other materials provided with the
            distribution.
        * Neither the name of pyglet nor the names of its
            contributors may be used to endorse or promote products
            derived from this software without specific prior written
            permission.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
    FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
    COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
    INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
    BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
    LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
    CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
    LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
    ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
    POSSIBILITY OF SUCH DAMAGE.
            """,
            x=440, y=165, anchor_x='center', anchor_y='center', font_size=8,
            bold=True, color=(255, 255, 255, 255),
            multiline=True, width=640, height=480
        )

        self.license_header = pyglet.text.Label("License", x=320, y=430,
                                                anchor_x='center',
                                                anchor_y='center',
                                                font_size=24, bold=True,
                                                color=(255, 255, 255, 255))

    def draw(self):
        bedroom.floor.draw()

        for obj in self.obj_list:
            if obj.sprite is not None and obj.visible:
                obj.sprite.draw()

        bedroom.b_neck_spr.draw()
        main_menu.dark.draw()

        if self.page == 1:
            self.license.draw()
            self.license_header.draw()
            self.page_right.draw()

        elif self.page == 2:
            self.controls.draw()
            self.page_left.draw()

        self.go_back.draw()

    def on_click(self, x, y, button):
        if self.back_region.contain(x, y):
            engine.set_next_screen(main_menu)

        if self.go_left_region.contain(x, y) and self.page == 2:
            self.page = 1

        elif self.go_right_region.contain(x, y) and self.page == 1:
            self.page = 2

    def on_key_press(self, symbol, modifiers):
        pass

    def update(self, dt):
        if self.back_region.contain(engine.mouse_X, engine.mouse_Y):
            window.set_mouse_cursor(choose_cur)

        if self.go_left_region.contain(engine.mouse_X, engine.mouse_Y) and \
           self.page == 2:
            window.set_mouse_cursor(choose_cur)

        if self.go_right_region.contain(engine.mouse_X, engine.mouse_Y) and \
           self.page == 1:
            window.set_mouse_cursor(choose_cur)


class Bedroom(Screen):

    floor = sprite.Sprite(playground_floor, x=0, y=0)
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

    def __init__(self):
        engine.layer = GAME
        self.obj_list = []
        self.mouse_over_button = False

        # Texts
        self.bed_text = text.Label(
            """
                   That bed looks comfy,
            but you don't feel like sleeping
            """, x=280, y=160,
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
             What game will you choose?
            """, x=280, y=230,
            anchor_x='center', anchor_y='center',
            font_size=24, color=(255, 255, 255, 255),
            multiline=True, width=562, height=357
        )

        self.message = None

    def draw(self):
        self.floor.draw()

        for obj in self.obj_list:
            if obj.sprite is not None and obj.visible:
                obj.sprite.draw()

        player.draw()
        self.b_neck_spr.draw()
        self.effect.draw()

        if engine.layer == MSG:
            engine.hud.popup.draw()
            self.message.draw()
            engine.hud.close_pop.draw()

            if self.mouse_over_button:
                engine.hud.popup_se.draw()
            else:
                engine.hud.popup_un.draw()

        main_music.pause()
        fish_music.pause()

        # Debugging
        ...

    def on_click(self, x, y, button):
        if engine.layer == MSG:

            if engine.hud.popup_button_region.contain(x, y):
                engine.hud.from_bag = False
                engine.layer = GAME

            if engine.hud.popup_button_region.contain(x, y) and \
               self.message == self.trash_text1:
                engine.layer = GAME
                player.games.append("fish")

            if engine.hud.popup_button_region.contain(x, y) and \
               self.message == self.game_text2:
                player.game_selected = "fish"

    def on_key_press(self, symbol, modifiers):
        if engine.layer == GAME and \
           engine.current_screen == bedroom:
            if player.is_over_bass and symbol == key.SPACE:
                bass_notes[randint(0, 12)].play()

            if player.is_over_bed and symbol == key.SPACE and \
               player.stamina > 1:
                select.play()
                engine.layer = MSG
                self.message = self.bed_text
                engine.showing_games = False

            elif (
                player.is_over_bed
                and symbol == key.SPACE
                and player.stamina <= 1
            ):
                clock.schedule_once(sleep, 3)
                player.is_sleeping = True
                player.x = 77
                player.y = 256

            if player.is_over_trash and symbol == key.SPACE \
               and "fish" not in player.games:
                select.play()
                engine.layer = MSG
                self.message = self.trash_text1
                engine.showing_games = False

            if player.is_over_trash and symbol == key.SPACE \
               and "fish" in player.games:
                select.play()
                engine.layer = MSG
                self.message = self.trash_text2
                engine.showing_games = False

            if player.is_over_desktop and symbol == key.SPACE \
               and "fish" not in player.games:
                select.play()
                engine.layer = MSG
                self.message = self.game_text1
                engine.showing_games = False

            if player.is_over_desktop and symbol == key.SPACE \
               and "fish" in player.games:
                select.play()
                engine.layer = MSG
                self.message = self.game_text2
                engine.showing_games = True

            if symbol == key.R:
                engine.began = False
                engine.layer = MENU
                engine.set_next_screen(main_menu)
                engine.showing_games = False

            if symbol == key.X:
                engine.set_next_screen(hall_upper)
                player.x = 600
                player.y = 70

    def update(self, dt):

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
        if engine.layer == MSG:

            if engine.hud.popup_button_region.contain(engine.mouse_X,
                                                      engine.mouse_Y):
                self.mouse_over_button = True
                window.set_mouse_cursor(choose_cur)
            else:
                self.mouse_over_button = False

    def is_key_pressed(self):
        for _k, v in keys.items():
            if v:
                return True

        return False


class HallUpper(Screen):

    bg = sprite.Sprite(hall1, x=0, y=0)

    def __init__(self):
        self.obj_list = []

    def draw(self):
        self.bg.draw()

        player.draw()

    def on_click(self, x, y, button):
        pass

    def on_key_press(self, symbol, modifiers):
        if symbol == key.P:
            engine.set_next_screen(bedroom)
            player.x = 50
            player.y = 70

    def update(self, dt):
        pass

    def is_key_pressed(self):
        for _k, v in keys.items():
            if v:
                return True

        return False



class FishingGame(Screen):

    menu = sprite.Sprite(fisher_menu, x=0, y=0)
    effect = sprite.Sprite(tv_effect, x=0, y=0)
    bg = sprite.Sprite(fisher_background, x=0, y=0)
    sea = sprite.Sprite(fisher_sea, x=0, y=0)
    fish_display = sprite.Sprite(fish, x=530, y=360)
    win_display = sprite.Sprite(fisher_won, x=0, y=0)
    lose_display = sprite.Sprite(fisher_lost, x=0, y=0)

    def __init__(self):
        self.enemies = []
        self.timer = 60
        self.fish_count = 0
        self.holding_fish = 0
        self.obj_list = []
        self.has_game_started = False
        self.game_finished = False
        self.won = False
        self.press_text = text.Label('Press ENTER to begin!',
                                     x=145, y=180, anchor_x='center',
                                     anchor_y='center', font_size=16,
                                     color=(255, 255, 255, 255),
                                     bold=True)

        self.goal_text = text.Label("""Your goal is to catch at least 10 fish
before the time runs out.""",
                                    x=320, y=430, anchor_x='center',
                                    anchor_y='center',
                                    font_size=14, color=(255, 255, 255, 255),
                                    bold=True)

        self.timer_text = text.Label(f"{self.timer}", x=320, y=380,
                                     anchor_x='center',
                                     anchor_y='center', font_size=24,
                                     color=(255, 255, 255, 255),
                                     bold=True)

        self.fish_text = text.Label(f"{self.fish_count}", x=570, y=380,
                                    anchor_x='center',
                                    anchor_y='center', font_size=24,
                                    color=(255, 255, 255, 255),
                                    bold=True)

        self.reminder_text = text.Label("""Remember to hold the fish for
enough time before catching!""",
                                        x=320, y=400, anchor_x='center',
                                        anchor_y='center',
                                        font_size=14,
                                        color=(255, 255, 255, 255), bold=True)

        self.fishing_rod_region = Region(player.fisherman.x - 10,
                                         player.fisherman.y - 1,
                                         50, 30)

        self.caught_something = False

    def draw(self):
        if not self.has_game_started and not self.game_finished:
            self.menu.draw()
            self.press_text.draw()

        if self.has_game_started and not self.game_finished:
            self.bg.draw()
            self.sea.draw()
            self.goal_text.draw()
            self.timer_text.draw()
            self.fish_text.draw()
            self.reminder_text.draw()
            self.fish_display.draw()
            fish_music.play()
            player.draw()

        if self.game_finished and not self.won:
            self.lose_display.draw()

        elif self.game_finished and self.won:
            self.win_display.draw()

        for obj in self.obj_list:
            if obj.sprite is not None and obj.visible:
                obj.sprite.draw()

        for enemy in self.enemies:
            enemy.draw()

        self.effect.draw()
        main_music.pause()

    def on_click(self, x, y, button):
        pass

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ENTER and not self.has_game_started:
            self.has_game_started = True
            self.game_finished = False
            self.won = False
            self.timer = 60
            self.fish_count = 0
            fisher_begin.play()
            player.x = 500
            player.y = 170
            self.begin_game()

        if symbol == key.BACKSPACE and not self.has_game_started:
            player.x = 320
            player.y = 148
            engine.layer = GAME
            engine.set_next_screen(bedroom)

        if symbol == key.SPACE and self.caught_something and \
           self.holding_fish >= 10 and not self.game_finished:
            self.enemies.remove(self.enemies[0])
            self.fish_count += 1
            got_fish.play()
            self.caught_something = False

        if symbol == key.SPACE and self.game_finished:
            self.has_game_started = True

        elif symbol == key.BACKSPACE and self.game_finished:
            player.x = 320
            player.y = 148
            engine.layer = GAME
            engine.set_next_screen(bedroom)

    def update(self, dt):
        if self.has_game_started and \
           engine.layer == FISHING:

            for enemy in self.enemies:
                enemy.update(dt)

            if keys[key.A]:
                if player.vx > -500:
                    player.vx -= 20

            if keys[key.D]:
                if player.vx < 500:
                    player.vx += 20

            self.fishing_rod_region.x = player.fisherman.x - 85
            self.fishing_rod_region.y = player.fisherman.y - 100

            self.detect_fish_collision()

            if self.timer <= 0 and self.fish_count < 10:
                self.end_game()
                fish_music.pause()
                fisher_lose.play()
                self.won = False

            elif self.timer <= 0 and self.fish_count >= 10:
                self.end_game()
                fish_music.pause()
                fisher_win.play()
                self.won = True

        self.update_text()

    def fish_timer(self, dt):
        self.timer -= 1

    def fish_spawner(self, dt):
        if len(self.enemies) == 0:
            new_enemy = Fish()
            self.enemies.append(new_enemy)

    def detect_fish_collision(self):
        if len(self.enemies) > 0:
            if self.fishing_rod_region.collides(self.enemies[0].region):
                self.holding_fish += 1
            else:
                self.caught_something = False
                self.holding_fish = 0

            if self.holding_fish >= 10:
                self.caught_something = True

    def is_key_pressed(self):
        for _k, v in keys.items():
            if v:
                return True

        return False

    def update_text(self):
        self.timer_text = text.Label(f"{self.timer}", x=320, y=360,
                                     anchor_x='center',
                                     anchor_y='center', font_size=24,
                                     color=(255, 255, 255, 255),
                                     bold=True)

        self.fish_text = text.Label(f"{self.fish_count}", x=570, y=360,
                                    anchor_x='center',
                                    anchor_y='center', font_size=24,
                                    color=(255, 255, 255, 255),
                                    bold=True)

        if self.fish_count > 9:
            self.fish_text.x = 560
            self.fish_display.x = 520

    def begin_game(self):
        clock.schedule_interval(fish_timer, 1)
        clock.schedule_interval(fish_spawner, randint(2, 6))

    def end_game(self):
        clock.unschedule(fish_timer)
        clock.unschedule(fish_spawner)
        self.timer = 60
        self.has_game_started = False
        self.caught_something = False
        self.game_finished = True
        fish_music.pause()

        if len(self.enemies) > 0:
            self.enemies.remove(self.enemies[0])


# Instances of classes
# Screens go first
player = Player()
fish = Fish()

# Bedroom objects
wall = SceneObject(id=0, solid=True, name="wall", x=320, y=372,
                   sprite=Bedroom.wall_spr)

bed = SceneObject(id=1, solid=True, name="bed", x=80, y=240,
                  sprite=Bedroom.bed_spr)

boundary_down = SceneObject(id=2, solid=True, name="b_bottom", x=320, y=0,
                            width=SCREENW, height=1)

boundary_left = SceneObject(id=3, solid=True, name="b_left", x=0, y=0, width=1,
                            height=SCREENH)

boundary_right = SceneObject(id=4, solid=True, name="b_right", x=639, y=0,
                             width=1, height=SCREENH)

body_bass = SceneObject(id=5, solid=True, name="bass_body", x=260, y=235,
                        sprite=Bedroom.b_body_spr)

outline_bass = SceneObject(id=6, solid=False, name="bass_outline", x=260,
                           y=285, width=87, height=205,
                           sprite=Bedroom.b_outline, visible=False)

outline_bed = SceneObject(id=7, solid=False, name="bed_outline", x=80, y=240,
                          sprite=Bedroom.bd_outline, visible=False)

trash = SceneObject(id=8, solid=True, name="trash_can", x=580, y=50,
                    sprite=Bedroom.trash)

outline_trash = SceneObject(id=9, solid=False, name="trash_outline", x=580,
                            y=50, width=80, height=80,
                            sprite=Bedroom.tr_outline, visible=False)

desktop = SceneObject(id=10, solid=True, name="desktop", x=480, y=255,
                      sprite=Bedroom.desk_spr)

outline_desktop = SceneObject(id=11, solid=False, name="desktop_outline",
                              x=480, y=255, width=190, height=125,
                              sprite=Bedroom.desk_out, visible=False)

# Fishing game objects
...

splash_screen = SplashScreen()
main_menu = MainMenu()
credit_screen = Credit()
engine = Engine(splash_screen)
bedroom = Bedroom()
hall_upper = HallUpper()
fishing_game = FishingGame()

# Add all the scene objects
main_menu.obj_list.append(bed)  # Main menu
main_menu.obj_list.append(body_bass)
main_menu.obj_list.append(trash)
main_menu.obj_list.append(desktop)

credit_screen.obj_list.append(wall)  # Credit screen
credit_screen.obj_list.append(bed)
credit_screen.obj_list.append(body_bass)
credit_screen.obj_list.append(trash)
credit_screen.obj_list.append(desktop)

bedroom.obj_list.append(wall)  # Bedroom
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

fishing_game.obj_list.append(boundary_left)  # Fishing game
fishing_game.obj_list.append(boundary_right)

target_width, target_height = target_resolution
viewport = FixedResolution(window,
                           target_width,
                           target_height)


@window.event
def on_draw():
    viewport.begin()
    window.clear()
    engine.draw()
    viewport.end()


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

    if engine.began and engine.layer == GAME and \
       not player.is_sleeping:
        # Normal movement
        if keys[key.W]:
            if player.stamina > 1:
                player.change_direction(0, 0, 170)
            else:
                player.change_direction(0, 0, 80)

            player.walking = True

        if keys[key.A]:
            if player.stamina > 1:
                player.change_direction(1, -170, 0)
            else:
                player.change_direction(1, -80, 0)

            player.walking = True

        if keys[key.S]:
            if player.stamina > 1:
                player.change_direction(1, 0, -170)
            else:
                player.change_direction(1, 0, -80)

            player.walking = True

        if keys[key.D]:
            if player.stamina > 1:
                player.change_direction(0, 170, 0)
            else:
                player.change_direction(0, 80, 0)

            player.walking = True

        # Diagonal implementation
        if keys[key.W] and keys[key.A]:
            if player.stamina > 1:
                player.change_direction(1, -160, 160)
            else:
                player.change_direction(1, -70, 70)

            player.walking = True

        if keys[key.W] and keys[key.D]:
            if player.stamina > 1:
                player.change_direction(0, 160, 160)
            else:
                player.change_direction(0, 70, 70)

            player.walking = True

        if keys[key.S] and keys[key.A]:
            if player.stamina > 1:
                player.change_direction(1, -160, -160)
            else:
                player.change_direction(1, -70, -70)
            player.walking = True

        if keys[key.S] and keys[key.D]:
            if player.stamina > 1:
                player.change_direction(0, 160, -160)
            else:
                player.change_direction(0, 70, -70)

            player.walking = True

        # Cancel two keys at the same time
        if keys[key.W] and keys[key.S]:
            player.change_direction(player.direction, 0, 0)
            player.walking = False

        if keys[key.A] and keys[key.D]:
            player.change_direction(player.direction, 0, 0)
            player.walking = False

        if not engine.current_screen.is_key_pressed():
            player.change_direction(player.direction, 0, 0)
            player.walking = False


@window.event
def fish_timer(dt):
    fishing_game.fish_timer(dt)


@window.event
def fish_spawner(dt):
    fishing_game.fish_spawner(dt)


@window.event
def sleep(dt):
    if player.is_sleeping:
        engine.enter()
        player.is_sleeping = False
        player.stamina = 5
        player.x = 320
        player.y = 148


@window.event
def stamina_drain(dt):
    if engine.layer == GAME and \
       engine.began and \
       player.stamina >= 1:
        player.stamina_drain(dt)


keys = key.KeyStateHandler()
window.push_handlers(keys)

clock.schedule_interval(update, 1/30)
clock.schedule_interval(stamina_drain, 1)

pyglet.app.run()
