import pygame as pg
from GameAssets import *

class GameFrame(object):
    """
    """

    def __init__(self, game_data):
        '''
        '''
        self.game_data = game_data

    def update(self, delta, keys):
        '''
        '''
        pass

    def render(self, screen):
        '''
        '''
        pass

class LevelFrame(GameFrame):
    """
    """

    def __init__(self, game_data):
        '''
        '''
        super().__init__(game_data)
        if self.game_data.save_index: self.game_data.load_save()
        else: self.game_data.load()
        self.game_data.load_level()

    def update(self, delta, keys):
        '''
        '''
        if keys[7]: self.game_data.switch_frame(PauseMenuFrame)
        self.game_data.update_collisions()
        for go in self.game_data.game_objects:
            go.update(delta, keys, self.game_data)

    def render(self, screen):
        '''
        '''
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
        if keys[7]:
            self.game_data.switch_frame(LevelFrame)

    def render(self, screen):
        '''
        '''
        dim = self.game_data.screen_dim
        text_0 = GameFonts.font_1.render("Pause Menu Press ESC", False, (255, 255, 255))
        screen.blit(text_0, (-text_0.get_width()/2 + dim[0]/2, -text_0.get_height()/2  + dim[1]/2))

class MainMenuFrame(GameFrame):
    """
    """

    def __init__(self, game_data):
        '''
        '''
        super().__init__(game_data)

    def update(self, delta, keys):
        '''
        '''
        if keys[0]:
            self.game_data.switch_frame(LevelFrame)

    def render(self, screen):
        '''
        '''
        dim = self.game_data.screen_dim
        text_0 = GameFonts.font_1.render("Main Menu Press Space", False, (255, 255, 255))
        screen.blit(text_0, (-text_0.get_width()/2 + dim[0]/2, -text_0.get_height()/2  + dim[1]/2))
