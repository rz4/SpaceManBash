import pygame as pg
import numpy as np
from GameAssets import GameAssets as ga
from GameObjects import *

class GameScripts:

    def script_0(update_args=None, render_args=None):
        '''
        '''
        if update_args is not None:
            update_args['game_data'].add_game_object(Teleporter([8300.0, 470.0, 1]))
            update_args['game_data'].add_game_object(Game_Message([8100.0, -1000.0, 200.0, 2000.0, "Jump on Teleporter to Exit Level"]))
            update_args['game_data'].remove_level_script("script_0")
