'''
GameData.py
Last Updated: 12/17/17

'''

import json, os
import numpy as np
import pygame as pg

class GameData():
    """
    GameData class is used to stores game state information.

    """

    def __init__(self):
        '''
        Method initiates game state variables.

        '''
        self.debug = True
        self.game_name = "SpaceManBash"
        self.delta_sum = 0

        # GameFrome Data
        self.frames = []
        self.frame_current = None

        # Configs
        self.screen_dim = (800, 600)
        self.controls = {
            'LEFT' : pg.K_a,
            'RIGHT' : pg.K_d,
            'UP' : pg.K_w,
            'DOWN' : pg.K_s,
            'CROUCH' : pg.K_LALT,
            'ATTACK' : pg.K_RSHIFT,
            'JUMP' : pg.K_SPACE,
            'SPRINT' : pg.K_LSHIFT,
            'PAUSE' : pg.K_ESCAPE,
            'ENTER' : pg.K_RETURN
        }

        # Save Data
        self.saves = []
        self.save_index = None

        # Level Data
        self.levels = []
        self.level_index = 0
        self.camera_pos = np.array([0.0, 0.0, 0.0, 0.0])
        self.camera_limits = [0.0, 0.0, 0.0, 0.0]
        self.game_objects = []
        self.collisions = {}

    def switch_frame(self, frame):
        '''
        Method switches current frame to desired frame. Instantiates desired
        frame if not found.

        Param:
            frame   ;GameFrame  new current frame

        '''
        for f in self.frames:
            if f.__class__.__name__ == frame:
                self.frame_current = f
                return
        module = __import__("GameFrames")
        class_ = getattr(module, frame)
        instance = class_(self)
        self.frames.append(instance)
        self.frame_current = self.frames[-1]

    def save_config(self, filename):
        '''
        Method saves game data configurations to file.

        Param:
            filename    ;str    config filename

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
        Method loads game data configurations to file.

        Param:
            filename    ;str    config filename

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

    def save_save(self, filename):
        '''
        Method saves game data state to save file.

        Param:
            filename    ;str    save filename

        '''
        try:
            with open("../data/" + self.saves[self.save_index], "w") as f:
                for level_data in self.levels:
                    json_dump = json.dumps(level_data)
                    f.write(json_dump + '\n')
        except Exception as e:
            print("Could Save Save Data:", filename)
            print(e)

    def load_save(self):
        '''
        Method loads game data state from save file.

        Param:
            filename    ;str    save filename
        '''
        try:
            with open("../data/" + self.saves[self.save_index], "r") as f:
                i = 0
                for data in f:
                    if i > 0: self.levels.append(level_data)
        except Exception as e:
            print("Could Load Save Data:", filename)
            print(e)

    def load(self):
        '''
        Method loads all game level data from file.

        '''
        for filename in sorted(os.listdir("../data/levels/")):
            if filename.endswith(".lev"):
                try:
                    with open("../data/levels/" + filename, "r") as f:
                        self.levels.append(f.read())
                except Exception as e:
                    print("Could Load Game Data:", filename)
                    print(e)

    def load_level(self):
        '''
        Method loads current level.

        '''
        try:
            data = json.loads(self.levels[self.level_index])
            self.camera_pos = np.array(data['camera_pos'])
            self.camera_limits = np.array(data['camera_limits'])
            for go in data['game_objects']:
                module = __import__("GameObjects")
                class_ = getattr(module, go[0])
                instance = class_(go[1:])
                self.add_game_object(instance)
        except Exception as e:
            print("Could Load Level:", self.level_index)
            print(e)

    def save_level(self):
        '''
        Method saves current level.

        '''
        pass

    def switch_level(self, index):
        '''
        Method switches level.

        Param:
            index   ;int    index of desired level

        '''
        self.level_index = index

    def add_game_object(self, game_object):
        '''
        Method adds game object.

        Param:
            game_object ;GameObject

        '''
        self.game_objects.append(game_object)

    def update_collisions(self):
        '''
        Method calculates collisions of game objects at current game state.
        Collisions are stored in self.collisions dictionary object.

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
        Method updates camera position to be centered on desired game object while
        remaining in the self.camera_limits boundaries.

        Param:
            game_object ;GameObject

        '''
        x = -(game_object.rect[0] + (game_object.rect[2]/2.0)) + (self.screen_dim[0]/2.0)
        y = -(game_object.rect[1] + (game_object.rect[3]/2.0)) + (self.screen_dim[1]/2.0)
        if x < self.camera_limits[2] and x > self.camera_limits[0]: self.camera_pos[0] = x
        if y < self.camera_limits[3] and y > self.camera_limits[1]: self.camera_pos[1] = y
