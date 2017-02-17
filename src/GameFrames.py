'''
GameFrame.py
Last Updated: 12/17/17

'''

import pygame as pg
from GameAssets import GameAnimations as ga
from GameAssets import GameFonts as gf

class GameFrame(object):
    """
    GameFrame class is used to define specific states of a game.
    For example, Level Frame is used when the game is running a game level
    or PauseMenuFrame when the game is running a pause menu.

    """

    def __init__(self, game_data):
        '''
        Method initiates game frame.

        Param:
            game_data   ;GameData  game data object pointer

        '''
        self.game_data = game_data

    def update(self, delta, keys):
        '''
        Method updates game frame.

        Param:
            delta   ;float  time past since last update in msec
            keys    ;int[]  array of binary values of actions being pressed

        '''
        pass

    def render(self, screen):
        '''
        Method renders game frame.

        Param:
            screen  ;pygame.screen
        '''
        pass

class LevelFrame(GameFrame):
    """
    """

    def __init__(self, game_data):
        '''
        Method initiates level frame by loading save data if exists else
        load fresh level data from levels folder. Loads in current level.

        '''
        super().__init__(game_data)
        if self.game_data.save_index: self.game_data.load_save()
        else: self.game_data.load()
        self.game_data.load_level()

    def update(self, delta, keys):
        '''
        '''
        # Change frame to puase menu if key 7 is pressed.
        if keys[2]: self.game_data.switch_frame("PauseMenuFrame")

        # Calculate collisions and update game objects
        self.game_data.update_collisions()
        for go in self.game_data.game_objects:
            go.update(delta, keys, self.game_data)

    def render(self, screen):
        '''
        '''
        # Render game objects
        for go in self.game_data.game_objects:
            go.render(screen, self.game_data)

class PauseMenuFrame(GameFrame):
    """
    """

    def __init__(self, game_data):
        '''
        '''
        super().__init__(game_data)

    def update(self, delta, keys):
        '''
        '''
        # Change frame to level frame if key 7 is pressed
        if keys[2]:
            self.game_data.switch_frame("LevelFrame")

    def render(self, screen):
        '''
        '''
        dim = self.game_data.screen_dim
        text_0 = gf.font_1.render("Pause Menu Press ESC", False, (255, 255, 255))
        screen.blit(text_0, (-text_0.get_width()/2 + dim[0]/2, -text_0.get_height()/2  + dim[1]/2))

class MainMenuFrame(GameFrame):
    """
    """

    def __init__(self, game_data):
        '''
        '''

        super(MainMenuFrame,self).__init__(game_data)


    def update(self, delta, keys):
        '''
        '''
        if keys[0]:
            self.game_data.switch_frame("LevelFrame")


    def render(self, screen):
        '''
        '''
        dim = self.game_data.screen_dim
        anim_width = ga.flame[0].get_width()
        anim_height = ga.flame[0].get_height()

        screen.blit(ga.space_img,(0,0))


        for i in range(anim_width,dim[0],(anim_width)*2):
            screen.blit(ga.animate(ga.flame, 10, self.game_data.delta_sum), (i, dim[1]-anim_height))
            screen.blit(ga.animate(ga.flame, 5, self.game_data.delta_sum), (i, 0))

        screen.blit(ga.animate(ga.mario_rest, 5, self.game_data.delta_sum), (-120+dim[0]*4/5, dim[1]/2-100))

        text_0 = gf.font_1.render("Main Menu", False, (255, 255, 255))
        text_1 = gf.font_1.render("Press Space", False, (255, 255, 255))
        screen.blit(text_0, (-text_0.get_width()/2 + dim[0]/2, -text_0.get_height()/2  + dim[1]*4/9))
        screen.blit(text_1, (-text_1.get_width()/2 + dim[0]/2, -text_1.get_height()/2  + dim[1]*5/9))
        screen.blit(ga.animate(ga.flame, 5, self.game_data.delta_sum), (-anim_width/2+dim[0]/3, -text_0.get_height()/2  + dim[1]*4/9))
        screen.blit(ga.animate(ga.flame, 5, self.game_data.delta_sum), (-anim_width/2+dim[0]*2/3, -text_0.get_height()/2  + dim[1]*4/9))
