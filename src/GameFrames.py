'''
GameFrame.py
Last Updated: 3/17/17

'''

import pygame as pg
from GameAssets import GameAssets as ga
from GameScripts import GameScripts as gs
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
            if self.level_loaded == False: return

        # Update script Stuff
        for script in self.game_data.level_scripts:
            script_ = getattr(gs, script)
            args = {}
            args['delta'] = delta
            args['keys'] = keys
            args['game_data'] = self.game_data
            script_(update_args=args)

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


        # Render script Stuff
        for script in self.game_data.level_scripts:
            script_ = getattr(gs, script)
            args = {}
            args['screen'] = screen
            args['game_data'] = self.game_data
            script_(render_args=args)

        # Render Game Information
        health = ga.font_3.render("Health: ", False, (255, 255, 255))
        if self.game_data.player_health > 60.0: color = (0, 255, 0)
        elif self.game_data.player_health > 30.0: color = (255, 255, 0)
        else: color = (255, 0, 0)
        h = ga.font_3.render(str(int(self.game_data.player_health)), False, color)
        screen.blit(health, (10, 10))
        screen.blit(h, (120, 10))

class PauseMenuFrame(GameFrame):
    """
    """
    def __init__(self, game_data):
        '''
        '''
        super().__init__(game_data)
        self.pointer = 0
        self.menu_limit = 2

        self.image_0 = ga.smb_left_idle.getCopy()
        self.image_0.scale2x()
        self.image_0.makeTransformsPermanent()
        self.image_0.play()

        self.image_1 = ga.es_right_idle.getCopy()
        self.image_1.scale2x()
        self.image_1.makeTransformsPermanent()
        self.image_1.play()

    def update(self, delta, keys):
        '''
        '''
        if keys[0]:
            if self.pointer == 0:
                ga.swing.play()
                self.game_data.switch_frame("LevelFrame")
            if self.pointer == 1:
                ga.swing.play()
                pg.mixer.music.fadeout(2000)
                Transitions.run("fadeOut", 1.5)
                while(True):
                    if Transitions.updateScreen() == False: break
                    pg.display.flip()
                self.game_data.switch_frame("MainMenuFrame")
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

        if self.pointer == 0: text_0 = ga.font_2.render("Continue", False,  (0, 255, 0))
        else: text_0 = ga.font_2.render("Continue", False, (255, 255, 255))
        if self.pointer == 1: text_1 = ga.font_2.render("Return To Main Menu", False,  (0, 255, 0))
        else: text_1 = ga.font_2.render("Return To Main Menu", False, (255, 255, 255))
        text_2 = ga.font_4.render("PAUSED", False, (255, 255, 255))

        self.image_0.blit(screen, (10, 200))
        self.image_1.blit(screen, (520, 215))

        screen.blit(text_0, (dim[0]/2.0 - (text_0.get_width()/2.0), 250))
        screen.blit(text_1, (dim[0]/2.0 - (text_1.get_width()/2.0), 300))
        screen.blit(text_2, (dim[0]/2.0 - (text_2.get_width()/2.0), 50))



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
                self.game_data.level_index = 0
                self.game_data.switch_frame("LevelFrame")
                self.game_data.reset_level()
            if self.pointer == 1:
                ga.swing.play()
                pg.mixer.music.fadeout(2000)
                Transitions.run("fadeOut", 2.5)
                while(True):
                    if Transitions.updateScreen() == False: break
                    pg.display.flip()
                self.game_data.load_save("save_0.sav")
                self.game_data.switch_frame("LevelFrame")
                self.game_data.reset_level()
            if self.pointer == 2:
                ga.swing.play()
                pg.mixer.music.fadeout(2000)
                Transitions.run("fadeOut", 2.5)
                while(True):
                    if Transitions.updateScreen() == False: break
                    pg.display.flip()
                self.game_data.running = False
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
        if self.pointer == 2: text_2 = ga.font_2.render("Quit", False,  (0, 255, 0))
        else: text_2 = ga.font_2.render("Quit", False, (255, 255, 255))
        info = ga.font_0.render("SpaceManBash V.1.0 - Script Kitties 2017", False, (255, 255, 255))

        screen.blit(text_0, (dim[0]/2.0 - (text_0.get_width()/2.0), 350))
        screen.blit(text_1, (dim[0]/2.0 - (text_1.get_width()/2.0), 400))
        screen.blit(text_2, (dim[0]/2.0 - (text_2.get_width()/2.0), 450))
        screen.blit(info, (dim[0]-260, dim[1]-20))
        screen.blit(ga.title, (100, 50))
