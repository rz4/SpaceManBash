'''
GameAssets.py
Last Updated: 12/17/17

'''

import pygame as pg
import pyganim

class GameAssets:

    font_0 = None
    font_1 = None
    font_2 = None

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
    title = None

    smb_left_idle = None
    smb_right_idle = None
    smb_left_run = None
    smb_right_run = None
    smb_left_jump = None
    smb_right_jump = None
    smb_left_hang = None
    smb_right_hang = None
    smb_swing_hang = None
    smb_swing_hang = None

    beep = None
    swing = None

    def init():
        '''
        '''
        pg.font.init()
        GameAssets.font_0 = pg.font.Font(None, 20)
        GameAssets.font_1 = pg.font.Font("../data/sprites/Gasalt-Black.ttf", 30)
        GameAssets.font_2 = pg.font.Font("../data/sprites/Gasalt-Regular.ttf", 40)

        GameAssets.space_img = SpriteSheet('../data/sprites/space.png').get_image(0,0,512,488)
        GameAssets.title = SpriteSheet('../data/sprites/title.png').get_image(0,0,512,488)

        GameAssets.flame = SpriteSheet('../data/sprites/space_fire.png').get_animation(782, 170, 24, 50, 4, 22, 50)
        #GameAssets.mario_rest = SpriteSheet('../data/sprites/mario_animations.png').get_animation(0, 0, 50, 30, 2, 50, 30)
        #GameAssets.mario_rest += SpriteSheet('../data/sprites/mario_animations.png').get_animation(0, 0, 50, 30, 2, 50, 30)
        #GameAssets.mario_slide = SpriteSheet('../data/sprites/mario_animations.png').get_animation(0, 0, 50, 30, 14, 50, 30)
        GameAssets.unicorn_still_left = SpriteSheet("../data/sprites/unicorn(1).png").get_animation(0, 0, 190, 125, 7, 160, 120,flip= True)
        GameAssets.unicorn_still_right = SpriteSheet("../data/sprites/unicorn(1).png").get_animation(0, 0, 190, 125, 7, 160, 120)
        GameAssets.unicorn_walk_left = SpriteSheet("../data/sprites/unicorn(1).png").get_animation(0, 150, 190, 125, 8, 160, 120,flip= True)
        GameAssets.unicorn_walk_right = SpriteSheet("../data/sprites/unicorn(1).png").get_animation(0, 150, 190, 125, 8, 160, 120)
        GameAssets.unicorn_attack_left = SpriteSheet("../data/sprites/unicorn(1).png").get_animation(0, 285, 190, 155, 7, 160, 120,flip= True)
        GameAssets.unicorn_attack_right = SpriteSheet("../data/sprites/unicorn(1).png").get_animation(0, 285, 190, 155, 7, 160, 120)
        GameAssets.unicorn_die_left = SpriteSheet("../data/sprites/unicorn(1).png").get_animation(0, 460, 175, 145, 7, 160, 120,flip= True)
        GameAssets.unicorn_die_right = SpriteSheet("../data/sprites/unicorn(1).png").get_animation(0, 460, 175, 145, 7, 160, 120)

        GameAssets.sheep_walk_left = SpriteSheet("../data/sprites/sheep.png").get_animation(119, 41, 40, 38, 3, 120, 120)
        GameAssets.sheep_walk_right = SpriteSheet("../data/sprites/sheep.png").get_animation(119, 41, 40, 38, 3, 120, 120, flip= True)
        GameAssets.sheep_attack_left = SpriteSheet("../data/sprites/sheep.png").get_animation(239, 361, 40, 38, 10, 120, 120)
        GameAssets.sheep_attack_right = SpriteSheet("../data/sprites/sheep.png").get_animation(239, 361, 40, 38, 10, 120, 120, flip= True)
        GameAssets.sheep_spin = SpriteSheet("../data/sprites/sheep.png").get_animation(0, 320, 40, 39, 16, 120, 120)

        GameAssets.dragon_still_left = SpriteSheet("../data/sprites/dragon.png").get_animation(7, 18, 60, 51, 6, 120, 120, flip=True)
        GameAssets.dragon_still_right = SpriteSheet("../data/sprites/dragon.png").get_animation(7, 18, 60, 51, 6, 120, 120)
        GameAssets.dragon_fly_left = SpriteSheet("../data/sprites/dragon.png").get_animation(7, 87, 80, 70, 2, 120, 120, flip=True)
        GameAssets.dragon_fly_right = SpriteSheet("../data/sprites/dragon.png").get_animation(7, 87, 80, 70, 2, 120, 120)
        GameAssets.dragon_fire_left = SpriteSheet("../data/sprites/dragon.png").get_animation(2, 157, 71, 60, 7, 120, 120, flip=True)
        GameAssets.dragon_fire_right = SpriteSheet("../data/sprites/dragon.png").get_animation(2, 157, 71, 60, 7, 120, 120)
        GameAssets.dragon_flame_left = SpriteSheet("../data/sprites/dragon.png").get_animation(323, 222, 68, 42, 4, 120, 120, flip=True)
        GameAssets.dragon_flame_right = SpriteSheet("../data/sprites/dragon.png").get_animation(323, 222, 68, 42, 4, 120, 120)
        GameAssets.dragon_die_left = SpriteSheet("../data/sprites/dragon.png").get_animation(167, 87, 80, 70, 2, 120, 120, flip=True)
        GameAssets.dragon_die_right = SpriteSheet("../data/sprites/dragon.png").get_animation(167, 87, 80, 70, 2, 120, 120)

        GameAssets.lava = SpriteSheet("../data/sprites/Lava_floor.png").get_animation(0, 0, 128, 138, 11, 120, 120)

        frames = pyganim.getImagesFromSpriteSheet("../data/sprites/smb_0.png", rows=1, cols=8, rects=[])
        GameAssets.smb_left_idle = pyganim.PygAnimation(list(zip(frames, [1000, 125, 700, 150, 2000, 5,800, 2000])))
        GameAssets.smb_right_idle = GameAssets.smb_left_idle.getCopy()
        GameAssets.smb_right_idle.flip(True, False)
        GameAssets.smb_right_idle.makeTransformsPermanent()
        GameAssets.smb_left_idle.play()
        GameAssets.smb_right_idle.play()

        frames = pyganim.getImagesFromSpriteSheet("../data/sprites/smb_1.png", rows=1, cols=8, rects=[])
        GameAssets.smb_left_run = pyganim.PygAnimation(list(zip(frames, [75 for i in range(8)])))
        GameAssets.smb_right_run = GameAssets.smb_left_run.getCopy()
        GameAssets.smb_right_run.flip(True, False)
        GameAssets.smb_right_run.makeTransformsPermanent()
        GameAssets.smb_left_run.play()
        GameAssets.smb_right_run.play()

        frames = pyganim.getImagesFromSpriteSheet("../data/sprites/smb_2.png", rows=1, cols=8, rects=[])
        GameAssets.smb_left_swing = pyganim.PygAnimation(list(zip(frames, [100, 55, 55, 55, 100, 100, 55, 55])), loop=False)
        GameAssets.smb_right_swing = GameAssets.smb_left_swing.getCopy()
        GameAssets.smb_right_swing.flip(True, False)
        GameAssets.smb_right_swing.makeTransformsPermanent()
        GameAssets.smb_left_swing.play()
        GameAssets.smb_right_swing.play()

        frames = pyganim.getImagesFromSpriteSheet("../data/sprites/smb_3.png", rows=1, cols=6, rects=[])
        GameAssets.smb_left_jump = pyganim.PygAnimation(list(zip(frames, [30, 20, 20, 100, 200, 5000])), loop=True)
        GameAssets.smb_right_jump = GameAssets.smb_left_jump.getCopy()
        GameAssets.smb_right_jump.flip(True, False)
        GameAssets.smb_right_jump.makeTransformsPermanent()
        GameAssets.smb_left_jump.play()
        GameAssets.smb_right_jump.play()

        frames = pyganim.getImagesFromSpriteSheet("../data/sprites/smb_4.png", rows=1, cols=6, rects=[])
        GameAssets.smb_left_hang = pyganim.PygAnimation(list(zip(frames, [2000, 200, 200, 200, 200, 200])), loop=True)
        GameAssets.smb_right_hang = GameAssets.smb_left_hang.getCopy()
        GameAssets.smb_right_hang.flip(True, False)
        GameAssets.smb_right_hang.makeTransformsPermanent()
        GameAssets.smb_left_hang.play()
        GameAssets.smb_right_hang.play()

        GameAssets.beep = pg.mixer.Sound("../data/music/beep.wav")
        GameAssets.swing = pg.mixer.Sound("../data/music/swing.wav")
        GameAssets.swing.set_volume(1.0)

    @staticmethod
    def animate(animation, speed, delta_sum):
        frame = int((int(delta_sum) / int(speed) ) % len(animation))
        return animation[frame]

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
