import pygame as pg
import numpy as np
import json, os
from GameFrames import *
from GameAssets import *
from GameObjects import *

class GameEngine():
    """
    """
    debug = True

    def __init__(self):
        '''
        '''
        # Load Game Data
        self.fps = 60
        self.config_filename = "../data/config.dat"
        self.game_data = GameData()
        self.game_data.load_config(self.config_filename)

        # Initiate Pygame
        pg.init()
        pg.display.set_caption("Script Kitties Game v0.0")
        self.screen = pg.display.set_mode(self.game_data.screen_dim)

        # Initiate Game
        self.game_data.switch_frame(MainMenuFrame)

    def run(self):
        '''
        '''
        running = True
        self.clock = pg.time.Clock()

        while running:
            key_events = [0 for i in range(len(self.game_data.controls))]

            # Key Pressed Events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                if event.type == pg.KEYDOWN:
                    if event.key == self.game_data.controls['ATTACK']:
                        key_events[0] = 1
                    if event.key == self.game_data.controls['PAUSE']:
                        key_events[7] = 1

            # Key Held Events
            pressed = pg.key.get_pressed()
            if pressed[self.game_data.controls['LEFT']]: key_events[1] = 1
            if pressed[self.game_data.controls['RIGHT']]: key_events[2] = 1
            if pressed[self.game_data.controls['UP']]: key_events[3] = 1
            if pressed[self.game_data.controls['DOWN']]: key_events[4] = 1
            if pressed[self.game_data.controls['CROUCH']]: key_events[5] = 1
            if pressed[self.game_data.controls['SPRINT']]: key_events[6] = 1


            delta = 1 / float(self.clock.tick(self.fps))
            self.update(delta, key_events)
            self.render()

            pg.display.flip()

        self.game_data.save_config(self.config_filename)

    def update(self, delta, keys):
        '''
        '''
        self.game_data.frame_index.update(delta, keys)

    def render(self):
        '''
        '''
        self.screen.fill((0, 0, 0))
        self.game_data.frame_index.render(self.screen)

        if GameEngine.debug:
            fps_text = GameFonts.font_0.render(str(int(self.clock.get_fps())), False, (255, 255, 255))
            self.screen.blit(fps_text, (780, 2))

class GameData():
    """
    """

    def __init__(self):
        '''
        '''
        # GameFrome Data
        self.frames = []
        self.frame_index = None

        # Configs
        self.screen_dim = (800, 600)
        self.controls = {
            'LEFT' : pg.K_a,
            'RIGHT' : pg.K_d,
            'UP' : pg.K_w,
            'DOWN' : pg.K_s,
            'CROUCH' : pg.K_LALT,
            'ATTACK' : pg.K_SPACE,
            'SPRINT' : pg.K_LSHIFT,
            'PAUSE' : pg.K_ESCAPE
        }

        # Save Data
        self.saves = []
        self.save_index = None

        # Level Data
        self.levels = []
        self.level_index = None

        self.camera_pos = np.array([0.0, 0.0, 0.0, 0.0])
        self.camera_limits = [-1000.0, 0.0, 1000.0, 1000.0]
        self.game_objects = []
        self.collisions = {}

    def switch_frame(self, frame):
        '''
        '''
        for f in self.frames:
            if f.__class__.__name__ == frame.__name__:
                self.frame_index = f
                return
        self.frames.append(frame(self))
        self.frame_index = self.frames[-1]

    def save_config(self, filename):
        '''
        '''
        try:
            with open("../data/" + filename, "w") as f:
                data = {}
                data['controls'] = self.controls
                data['screen_dim'] = self.screen_dim
                data['save_filenames'] = self.saves
                json_dump = json.dumps(data)
                f.write(json_dump)
        except Exception as e:
            print("Could Save Config:", filename)
            print(e)

    def load_config(self, filename):
        '''
        '''
        try:
            with open("../data/" + filename, "r") as f:
                for json_dump in f:
                    data = json.loads(json_dump)
                    self.controls = data['controls']
                    self.screen_dim = data['screen_dim']
                    self.saves = data['save_filenames']
        except Exception as e:
            print("Could Load Config:", filename)
            print(e)

    def save_save(self):
        '''
        '''
        try:
            with open("../data/saves/" + self.saves[self.save_index], "w") as f:
                for level_data in self.levels:
                    json_dump = json.dumps(level_data)
                    f.write(json_dump + '\n')
        except Exception as e:
            print("Could Save Save Data:", filename)
            print(e)

    def load_save(self):
        '''
        '''
        try:
            with open("../data/saves/" + self.saves[self.save_index], "r") as f:
                i = 0
                for data in f:
                    if i > 0: self.levels.append(level_data)
        except Exception as e:
            print("Could Load Save Data:", filename)
            print(e)

    def load(self):
        '''
        '''
        for filename in os.listdir("../data/levels/"):
            if filename.endswith(".lev"):
                try:
                    with open("../data/levels/" + filename, "r") as f:
                        self.levels.append(f.read())
                except Exception as e:
                    print("Could Load Game Data:", filename)
                    print(e)
        self.level_index = 0

    def load_level(self):
        '''
        '''
        #try:
        data = json.loads(self.levels[self.level_index])
        self.camera_pos = np.array(data['camera_pos'])
        for go in data['game_objects']:
            module = __import__("GameObjects")
            class_ = getattr(module, go[0])
            instance = class_(go[1:])
            self.add_game_object(instance)
        #except Exception as e:
        #    print("Could Load Level:", self.level_index)
        #    print(e)

    def save_level(self):
        '''
        '''
        pass

    def switch_level(self, index):
        '''
        '''
        self.level_index = index

    def add_game_object(self, game_object):
        '''
        '''
        self.game_objects.append(game_object)

    def update_collisions(self):
        '''
        '''
        self.collisions = {}
        for go in self.game_objects:
            temp = []
            for goo in self.game_objects:
                if go != goo and go.check_collision(goo.rect):
                    temp.append(goo)
            self.collisions[go] = temp

    def center_camera_on_game_object(self, game_object):
        '''
        '''
        x = -(game_object.rect[0] + (game_object.rect[2]/2.0)) + (self.screen_dim[0]/2.0)
        y = -(game_object.rect[1] + (game_object.rect[3]/2.0)) + (self.screen_dim[1]/2.0)
        if x < self.camera_limits[2] and x > self.camera_limits[0]: self.camera_pos[0] = x
        if y < self.camera_limits[3] and y > self.camera_limits[1]: self.camera_pos[1] = y


if __name__ == '__main__':
    game = GameEngine()
    game.run()
