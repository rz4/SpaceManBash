'''
GameFrame.py
Last Updated: 3/17/17

'''

import pygame as pg
from GameAssets import GameAssets as ga
import GameObjects
import Transitions

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
        self.game_data.load_level()
        self.level_loaded = False

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
        # Render Level Transition
        if not self.level_loaded:
            screen.fill((0,0,0))
            text = ga.font_1.render("Level " + str(self.game_data.level_index), False, (255, 255, 255))
            screen.blit(text, (350, 250))
            Transitions.run("fadeIn", 2.5)
            while(True):
                if Transitions.updateScreen() == False: break
                pg.display.flip()
            Transitions.run("fadeOut", 2.5)
            while(True):
                if Transitions.updateScreen() == False: break
                pg.display.flip()
            self.level_loaded = True
            return

        cam_pos = self.game_data.camera_pos.astype(int)

        # Render Backgrounds
        screen.blit(self.game_data.level_background, (cam_pos[0]/5,cam_pos[1]/5-100))
        screen.blit(self.game_data.level_midground, (cam_pos[0]/3,cam_pos[1]/3-200))

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
        self.acc = 0
        self.anim_cycle = 0

    def update(self, delta, keys):
        '''
        '''
        if keys[0]:
            self.game_data.switch_frame("LevelFrame")
        if keys[10]:
            self.game_data.load_level
            self.game_data.switch_frame("MainMenuFrame")

        if self.acc < 1:
            self.acc += delta
        else:
            self.acc = 0
            if self.anim_cycle < 4:
                self.anim_cycle += 1
            else: self.anim_cycle = 0

    def render(self, screen):
        '''
        '''
        dim = self.game_data.screen_dim

        space_img = pg.transform.scale(ga.background_0, (dim[0], dim[1]))
        screen.blit(space_img,(0,0))

        text_0 = ga.font_1.render("Pause Menu", False, (255, 255, 255))
        screen.blit(text_0, (-text_0.get_width()/2 + dim[0]/2, -text_0.get_height()/2  + dim[1]/4))

        text_0 = ga.font_1.render("To return to game", False, (0, 255, 255))
        text_1 = ga.font_1.render("Press SPACE", False, (0, 255, 255))
        screen.blit(text_0, (-text_0.get_width()/2 + dim[0]/4, -text_0.get_height()/2  + dim[1]*4/9))
        screen.blit(text_1, (-text_1.get_width()/2 + dim[0]/4, -text_1.get_height()/2  + dim[1]*5/9))

        text_0 = ga.font_1.render("For main menu", False, (0, 255, 255))
        text_1 = ga.font_1.render("Press H", False, (0, 255, 255))
        screen.blit(text_0, (-text_0.get_width()/2 + dim[0]*3/4, -text_0.get_height()/2  + dim[1]*4/9))
        screen.blit(text_1, (-text_1.get_width()/2 + dim[0]*3/4, -text_1.get_height()/2  + dim[1]*5/9))

class MainMenuFrame(GameFrame):
    """
    """

    def __init__(self, game_data):
        '''
        '''
        super(MainMenuFrame,self).__init__(game_data)
        self.menu_limit = 3
        self.pointer = 0

    def update(self, delta, keys):
        '''
        '''
        if keys[0]:
            if self.pointer == 0:
                ga.swing.play()
                pg.mixer.music.fadeout(2000)
                Transitions.run("fadeOut", 2.5)
                while(True):
                    if Transitions.updateScreen() == False: break
                    pg.display.flip()
                self.game_data.switch_frame("LevelFrame")
            self.pointer = 0

        if keys[12] and self.pointer > 0:
            self.pointer -= 1
            ga.beep.play()
        if keys[13] and self.pointer < self.menu_limit-1:
            self.pointer += 1
            ga.beep.play()

    def render(self, screen):
        '''
        '''
        dim = self.game_data.screen_dim

        if self.pointer == 0: text_0 = ga.font_2.render("New Game", False,  (0, 255, 0))
        else: text_0 = ga.font_2.render("New Game", False, (255, 255, 255))
        if self.pointer == 1: text_1 = ga.font_2.render("Continue", False,  (0, 255, 0))
        else: text_1 = ga.font_2.render("Continue", False, (255, 255, 255))
        if self.pointer == 2: text_2 = ga.font_2.render("Options", False,  (0, 255, 0))
        else: text_2 = ga.font_2.render("Options", False, (255, 255, 255))
        info = ga.font_0.render("SpaceManBash V.1.0 - Script Kitties 2017", False, (255, 255, 255))

        screen.blit(text_0, (325, 350))
        screen.blit(text_1, (325, 400))
        screen.blit(text_2, (325, 450))
        screen.blit(info, (dim[0]-260, dim[1]-20))
        screen.blit(ga.title, (100, 50))
