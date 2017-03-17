'''
GameAssets.py
Last Updated: 12/17/17

'''

import pygame as pg
import pyganim

class GameAssets:

    def init(dim):
        '''
        '''

        # Load Fonts
        pg.font.init()
        GameAssets.font_0 = pg.font.Font(None, 20)
        GameAssets.font_1 = pg.font.Font("../data/sprites/Gasalt-Black.ttf", 30)
        GameAssets.font_2 = pg.font.Font("../data/sprites/Gasalt-Regular.ttf", 40)

        # Load Static Images
        GameAssets.title = pg.image.load("../data/sprites/title.png").convert()
        GameAssets.title.set_colorkey((0, 0, 0))

        GameAssets.wall = pg.image.load('../data/sprites/metal_block.png').convert()

        GameAssets.background_0 = pg.image.load("../data/sprites/space2.png").convert()
        GameAssets.background_0 = pg.transform.scale(GameAssets.background_0, (dim[0]+900,  dim[1]+100))

        GameAssets.midground_0 = pg.image.load("../data/sprites/stationbckground.png").convert()
        GameAssets.midground_0 = pg.transform.scale(GameAssets.midground_0, (dim[0]+2000,  dim[1]+500))
        GameAssets.midground_0.set_colorkey((0, 0, 0))

        # Load Animations

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

        frames = pyganim.getImagesFromSpriteSheet("../data/sprites/Lava_floor.png", rows=1, cols=11, rects=[])
        GameAssets.lava = pyganim.PygAnimation(list(zip(frames, [200 for i in range(11)])))
        GameAssets.lava.set_colorkey((0,0,0))
        GameAssets.lava.play()

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
        GameAssets.smb_left_swing = pyganim.PygAnimation(list(zip(frames, [30, 30, 30, 20, 100, 55, 30, 30])), loop=False)
        GameAssets.smb_right_swing = GameAssets.smb_left_swing.getCopy()
        GameAssets.smb_right_swing.flip(True, False)
        GameAssets.smb_right_swing.makeTransformsPermanent()
        GameAssets.smb_left_swing.play()
        GameAssets.smb_right_swing.play()

        frames = pyganim.getImagesFromSpriteSheet("../data/sprites/smb_5.png", rows=1, cols=8, rects=[])
        GameAssets.smb_left_bash = pyganim.PygAnimation(list(zip(frames, [30, 30, 30, 30, 20, 20, 20, 100])), loop=False)
        GameAssets.smb_right_bash = GameAssets.smb_left_bash.getCopy()
        GameAssets.smb_right_bash.flip(True, False)
        GameAssets.smb_right_bash.makeTransformsPermanent()
        GameAssets.smb_left_bash.play()
        GameAssets.smb_right_bash.play()

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

        frames = pyganim.getImagesFromSpriteSheet("../data/sprites/smb_6.png", rows=1, cols=8, rects=[])
        GameAssets.smb_left_death = pyganim.PygAnimation(list(zip(frames, [200, 100, 100, 100, 100, 100, 100, 1200])))
        GameAssets.smb_right_death = GameAssets.smb_left_death.getCopy()
        GameAssets.smb_right_death.flip(True, False)
        GameAssets.smb_right_death.makeTransformsPermanent()
        GameAssets.smb_left_death.play()
        GameAssets.smb_right_death.play()

        frames = pyganim.getImagesFromSpriteSheet("../data/sprites/es_0.png", rows=1, cols=8, rects=[])
        GameAssets.es_left_idle = pyganim.PygAnimation(list(zip(frames, [120 for i in range(8)])))
        GameAssets.es_right_idle = GameAssets.es_left_idle.getCopy()
        GameAssets.es_right_idle.flip(True, False)
        GameAssets.es_right_idle.makeTransformsPermanent()
        GameAssets.es_left_idle.play()
        GameAssets.es_right_idle.play()

        frames = pyganim.getImagesFromSpriteSheet("../data/sprites/es_1.png", rows=1, cols=8, rects=[])
        GameAssets.es_left_jump = pyganim.PygAnimation(list(zip(frames, [100 for i in range(8)])))
        GameAssets.es_right_jump = GameAssets.es_left_jump.getCopy()
        GameAssets.es_right_jump.flip(True, False)
        GameAssets.es_right_jump.makeTransformsPermanent()
        GameAssets.es_left_jump.play()
        GameAssets.es_right_jump.play()

        frames = pyganim.getImagesFromSpriteSheet("../data/sprites/es_2.png", rows=1, cols=10, rects=[])
        GameAssets.es_left_shock = pyganim.PygAnimation(list(zip(frames, [500, 100, 100, 100, 100, 100, 100, 100, 100, 100])))
        GameAssets.es_right_shock = GameAssets.es_left_shock.getCopy()
        GameAssets.es_right_shock.flip(True, False)
        GameAssets.es_right_shock.makeTransformsPermanent()
        GameAssets.es_left_shock.play()
        GameAssets.es_right_shock.play()

        frames = pyganim.getImagesFromSpriteSheet("../data/sprites/es_3.png", rows=1, cols=10, rects=[])
        GameAssets.es_left_death = pyganim.PygAnimation(list(zip(frames, [120 for i in range(10)])))
        GameAssets.es_right_death = GameAssets.es_left_death.getCopy()
        GameAssets.es_right_death.flip(True, False)
        GameAssets.es_right_death.makeTransformsPermanent()
        GameAssets.es_left_death.play()
        GameAssets.es_right_death.play()

        # Load Music
        GameAssets.beep = pg.mixer.Sound("../data/music/beep.wav")
        GameAssets.swing = pg.mixer.Sound("../data/music/swing.wav")
        GameAssets.jump = pg.mixer.Sound("../data/music/jump.wav")
        GameAssets.swing.set_volume(1.0)
        GameAssets.jump.set_volume(0.1)

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
