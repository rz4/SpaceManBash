'''
GameAssets.py
Last Updated: 12/17/17

'''

import pygame as pg

class SpriteSheet():
    """ Class used to grab images out of a sprite sheet. """

    def __init__(self, file_name):
        """ Constructor. Pass in the file name of the sprite sheet. """

        # Load the sprite sheet.
        self.sprite_sheet = pg.image.load(file_name).convert()


    def get_image(self, x, y, width, height):
        """ Grab a single image out of a larger spritesheet
            Pass in the x, y location of the sprite
            and the width and height of the sprite. """

        # Create a new blank image
        image = pg.Surface([width, height]).convert()

        # Copy the sprite from the large sheet onto the smaller image
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))

        # Assuming black works as the transparent color
        image.set_colorkey((0, 0, 0))

        # Return the image
        return image

    def get_animation(self, x, y, width, height, frames, scale_x, scale_y, flip=False):
        animation = []

        for i in range(frames):
            image = self.get_image(x + (i * width), y, width, height)
            image = pg.transform.scale(image, (scale_x, scale_y))
            image = pg.transform.flip(image, flip, False)
            animation.append(image)

        return animation

class GameFonts:
    """
    GameFonts stores fonts used for game.

    """
    font_0 = None
    font_1 = None

    def init():
        '''
        '''
        pg.font.init()
        GameFonts.font_0 = pg.font.SysFont("Comic Sans MS", 20)
        GameFonts.font_1 = pg.font.SysFont("Comic Sans MS", 30)

class GameAnimations:
    """
    GameAnimations class stores sprite animations used for game.

    """
    player_walk_left = None
    player_walk_left = None
    player_still_left = None
    player_still_left = None
    player_jump_left = None
    player_jump_left = None
    player_falling_left = None
    player_falling_right = None

    flame = None

    mario_rest = None
    mario_slide = None

    unicorn_walk_left = None
    unicorn_walk_right = None
    unicorn_walk_left = None
    unicorn_walk_right =None
    unicorn_walk_left = None
    unicorn_walk_right = None
    unicorn_walk_left = None
    unicorn_walk_right = None

    space_img = None

    @staticmethod
    def init():
        '''
        '''
        GameAnimations.player_walk_left = SpriteSheet("../data/sprites/am2r_walk.png").get_animation(1, 9, 41, 36, 10, 123, 116)
        GameAnimations.player_walk_right = SpriteSheet("../data/sprites/am2r_walk.png").get_animation(3, 57, 41, 36, 10, 123, 116)
        GameAnimations.player_still_left = SpriteSheet("../data/sprites/am2r_still.png").get_animation(198, 7, 41, 38, 1, 123, 116)
        GameAnimations.player_still_right = SpriteSheet("../data/sprites/am2r_still.png").get_animation(242, 7, 41, 38, 1, 123, 116)
        GameAnimations.player_jump_left = SpriteSheet("../data/sprites/am2r_still.png").get_animation(110, 500, 41, 33, 1, 123, 99)
        GameAnimations.player_jump_right = SpriteSheet("../data/sprites/am2r_still.png").get_animation(70, 500, 41, 33, 1, 123, 99)
        GameAnimations.player_falling_left = SpriteSheet("../data/sprites/am2r_still.png").get_animation(159, 499, 41, 33, 1, 123, 99)
        GameAnimations.player_falling_right = SpriteSheet("../data/sprites/am2r_still.png").get_animation(200, 499, 41, 33, 1, 123, 99)
        GameAnimations.flame = SpriteSheet('../data/sprites/space_fire.png').get_animation(785, 170, 22, 50, 5, 22, 50)
        GameAnimations.mario_rest = SpriteSheet('../data/sprites/mario_animations.png').get_animation(0, 0, 50, 30, 14, 50, 30)
        GameAnimations.mario_slide = SpriteSheet('../data/sprites/mario_animations.png').get_animation(501, 1, 30, 50, 14, 30, 50)
        GameAnimations.unicorn_walk_left = SpriteSheet("../data/sprites/Unicorn.png").get_animation(0, 156, 125, 100, 8, 123, 116)
        GameAnimations.unicorn_walk_right = SpriteSheet("../data/sprites/Unicorn.png").get_animation(0, 156, 125, 100, 8, 123, 116,flip= True)
        GameAnimations.unicorn_walk_left = SpriteSheet("../data/sprites/Unicorn.png").get_animation(0, 34, 100, 100, 9, 123, 116)
        GameAnimations.unicorn_walk_right = SpriteSheet("../data/sprites/Unicorn.png").get_animation(0, 34, 100, 100, 9, 123, 116,flip= True)
        GameAnimations.unicorn_walk_left = SpriteSheet("../data/sprites/Unicorn.png").get_animation(-30, 264, 150, 100, 9, 133, 116)
        GameAnimations.unicorn_walk_right = SpriteSheet("../data/sprites/Unicorn.png").get_animation(-30, 264, 150, 100, 9, 133, 116,flip= True)
        GameAnimations.unicorn_walk_left = SpriteSheet("../data/sprites/Unicorn.png").get_animation(0, 156, 125, 100, 8, 123, 116)
        GameAnimations.unicorn_walk_right = SpriteSheet("../data/sprites/Unicorn.png").get_animation(0, 156, 125, 100, 8, 123, 116,flip= True)
        GameAnimations.space_img = SpriteSheet('../data/sprites/space.png').get_image(0,0,512,488)

    @staticmethod
    def animate(animation, speed, delta_sum):
        frame = int((int(delta_sum) / int(speed) ) % len(animation))
        return animation[frame]
