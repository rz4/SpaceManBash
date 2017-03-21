'''
GameEngine.py
Last Updated: 12/17/17

'''

import pygame as pg
from GameAssets import GameAssets as ga
from GameData import GameData
import Transitions

class GameEngine():
    """
    GameEngine class is used to interface with the pygame package.

    """

    def __init__(self, config):
        '''
        Method initiates game and assets.

        Param:
            config  ;str    filename of config file.

        '''
        # Load Game Data
        self.fps = 60
        self.config_filename = config
        self.game_data = GameData()
        self.game_data.load_config(self.config_filename)
        self.game_data.load_game_data()

        # Initiate Pygame
        pg.init()
        pg.mixer.init()
        pg.display.set_caption(self.game_data.game_name)
        self.screen = pg.display.set_mode(self.game_data.screen_dim)
        Transitions.init(self.screen, self.game_data.screen_dim[0], self.game_data.screen_dim[1], [0,0,0])

        #Initiate Game Assets
        ga.init(self.game_data.screen_dim)

    def run(self):
        '''
        Method runs game loop.

        '''
        self.clock = pg.time.Clock()

        # Intro Animation
        if self.game_data.debug == False:
            logo = pg.image.load("../doc/logo.png").convert()
            logo.set_colorkey((0, 0, 0))
            self.screen.fill((252,240,228))
            self.screen.blit(logo, (250, 150))

            Transitions.run("fadeIn", 1.5)
            while(True):
                if Transitions.updateScreen() == False: break
                self.clock.tick(self.fps)
                pg.display.flip()

            ga.yee.play()
            pg.time.wait(2000)

            Transitions.run("fadeOut", 1.5)
            while(True):
                if Transitions.updateScreen() == False: break
                self.clock.tick(self.fps)
                pg.display.flip()

            pg.time.wait(1000)

            self.screen.fill((0,0,0))
            text = ga.font_1.render("Script Kitties Entertainment Presents", False, (255, 255, 255))
            self.screen.blit(text, (200, 250))

            pg.mixer.music.load("../data/music/test.mp3")
            pg.mixer.music.set_volume(0.15)
            pg.mixer.music.play()

            Transitions.run("fadeIn", 1.5)
            while(True):
                if Transitions.updateScreen() == False: break
                self.clock.tick(self.fps)
                pg.display.flip()

            pg.time.wait(1500)

            Transitions.run("fadeOut",  1.5)
            while(True):
                if Transitions.updateScreen() == False: break
                self.clock.tick(self.fps)
                pg.display.flip()

            pg.time.wait(2000)

            self.render()
            Transitions.run("fadeInSpin", 2)
            Transitions.updateScreen()
            self.clock.tick(self.fps)

        #Game Loop
        while self.game_data.running:
            # Key Events
            key_events = [0 for i in range(len(self.game_data.controls)+4)]

            # Key Pressed Events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.game_data.running = False
                if event.type == pg.KEYDOWN:
                    if event.key == self.game_data.controls['JUMP']:
                        key_events[0] = 1
                    if event.key == self.game_data.controls['ATTACK']:
                        key_events[1] = 1
                    if event.key == self.game_data.controls['ALTATTACK']:
                        key_events[11] = 1
                    if event.key == self.game_data.controls['PAUSE']:
                        key_events[2] = 1
                    if event.key == self.game_data.controls['ENTER']:
                        key_events[3] = 1
                    if event.key == self.game_data.controls['UP']:
                        key_events[12] = 1
                    if event.key == self.game_data.controls['DOWN']:
                        key_events[13] = 1
                    if event.key == self.game_data.controls['LEFT']:
                        key_events[14] = 1
                    if event.key == self.game_data.controls['RIGHT']:
                        key_events[15] = 1

            # Key Held Events
            pressed = pg.key.get_pressed()
            if pressed[self.game_data.controls['LEFT']]: key_events[4] = 1
            if pressed[self.game_data.controls['RIGHT']]: key_events[5] = 1
            if pressed[self.game_data.controls['UP']]: key_events[6] = 1
            if pressed[self.game_data.controls['DOWN']]: key_events[7] = 1
            if pressed[self.game_data.controls['CROUCH']]: key_events[8] = 1
            if pressed[self.game_data.controls['SPRINT']]: key_events[9] = 1
            if pressed[self.game_data.controls['HOME']]: key_events[10] = 1

            #Update and Render Game State

            if Transitions.updateScreen() == False:
                delta = 1 / float(self.clock.tick(self.fps))
                self.game_data.delta_sum += 1
                if self.game_data.delta_sum > 10000: self.game_data.delta_sum = 0
                self.update(delta, key_events)
                self.render()
            else:
                self.clock.tick(self.fps)

            # Debugging Information
            if self.game_data.debug:
                fps_text = ga.font_0.render(str(int(self.clock.get_fps())), False, (255, 255, 255))
                self.screen.blit(fps_text, (780, 2))

            pg.display.flip()

        self.game_data.save_config(self.config_filename)

    def update(self, delta, keys):
        '''
        Method used to update game state.

        Param:
            delta   ;float  time past since last update in msec
            keys    ;int[]  array of binary values of actions being pressed

        '''
        self.game_data.frame_current.update(delta, keys)

    def render(self):
        '''
        Method used to render game state.

        '''
        self.screen.fill((0,0,0))
        if self.game_data.running: self.game_data.frame_current.render(self.screen)
