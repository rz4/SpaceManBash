'''
GameData.py
Last Updated: 3/16/17

'''

import json, os
import numpy as np
import pygame as pg
from GameAssets import GameAssets as ga

class GameData():
    """
    GameData class is used to stores game state information.

    """

    def __init__(self):
        '''
        Method initiates game state variables.

        '''
        self.debug = False
        self.game_name = "SpaceManBash"
        self.delta_sum = 0
        self.running = True

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
            'ATTACK' : pg.K_j,
            'ALTATTACK' : pg.K_k,
            'JUMP' : pg.K_SPACE,
            'SPRINT' : pg.K_LSHIFT,
            'PAUSE' : pg.K_ESCAPE,
            'ENTER' : pg.K_RETURN,
            'HOME' : pg.K_h
        }

        # Save Data
        self.saves = []
        self.save_index = None

        # Level Data
        self.levels = []
        self.level_index = 0
        self.level_background = None
        self.level_midground = None
        self.camera_pos = np.array([0.0, 0.0, 0.0, 0.0])
        self.camera_limits = [0.0, 0.0, 0.0, 0.0]
        self.game_objects = []
        self.collisions = {}
        self.level_scripts = []
        self.script_vars = {}

        # Player Data
        self.player_pos = np.array([0.0, 0.0])
        self.player_health = 100

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
            with open("../data/saves/" + filename, "w") as f:
                data = {}
                data["level_index"] = self.level_index
                json_dump = json.dumps(data)
                f.write(json_dump + '\n')
        except Exception as e:
            print("Could Save Save Data:", filename)
            print(e)

    def load_save(self, filename):
        '''
        Method loads game data state from save file.

        Param:
            filename    ;str    save filename
        '''
        try:
            with open("../data/saves/" + filename, "r") as f:
                for json_dump in f:
                    data = json.loads(json_dump)
                    self.level_index = data["level_index"]
        except Exception as e:
            print("Could Load Save Data:", filename)
            print(e)

    def load_game_data(self):
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
            pg.mixer.music.load("../data/music/"+data['music'])
            pg.mixer.music.set_volume(0.15)
            pg.mixer.music.play(loops=3)
            self.level_background = getattr(ga, data['background'])
            self.level_midground = getattr(ga, data['midground'])
            for script in data['scripts']: self.add_level_script(script)
        except Exception as e:
            print("Couldn't Load Level:", self.level_index)
            print(e)

    def reset_level(self):
        '''
        Method resets current level.

        '''
        self.frame_current.level_loaded = False
        self.game_objects = []
        self.collisions = {}
        self.load_level()

    def switch_level(self, index):
        '''
        Method switches level.

        Param:
            index   ;int    index of desired level

        '''
        self.level_index = index
        self.frame_current.level_loaded = False
        self.game_objects = []
        self.collisions = {}
        self.save_save("save_0.sav")
        self.load_level()

    def add_game_object(self, game_object):
        '''
        Method adds game object.

        Param:
            game_object ;GameObject

        '''
        self.game_objects.append(game_object)

    def remove_game_object(self, game_object):
        '''
        Method adds game object.

        Param:
            game_object ;GameObject

        '''
        self.game_objects.remove(game_object)

    def add_level_script(self, script):
        '''
        '''
        self.level_scripts.append(script)

    def remove_level_script(self, script):
        '''
        '''
        self.level_scripts.remove(script)

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
