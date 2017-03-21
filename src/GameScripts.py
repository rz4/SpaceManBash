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

    def script_1(update_args=None, render_args=None):
        '''
        '''
        if update_args is not None:
            if 'sheeps' in update_args['game_data'].script_vars:
                i = 0
                for go in update_args['game_data'].game_objects:
                    if go.__class__.__name__ == "Electric_Sheep": i +=1
                if update_args['game_data'].script_vars['sheeps'] < 1000:
                    if i < 4:
                        if update_args['game_data'].delta_sum%100 == 0:
                            update_args['game_data'].add_game_object(Electric_Sheep([1000.0, 200.0, 0.5]))
                            update_args['game_data'].script_vars['sheeps'] += 1
                else:
                    update_args['game_data'].add_game_object(Teleporter([8300.0, 470.0, 0]))
                    update_args['game_data'].remove_level_script("script_1")
            else:
                update_args['game_data'].script_vars['sheeps'] = 0
                update_args['game_data'].add_game_object(Game_Message([0.0, -1000.0, 2000.0, 2000.0, "Kill All The Sheep!"]))
