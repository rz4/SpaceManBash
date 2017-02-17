import pygame as pg
pg.font.init()

class GameFonts():

    font_0 = pg.font.SysFont("Comic Sans MS", 20)
    font_1 = pg.font.SysFont("Comic Sans MS", 30)

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

    def get_animation(self, x, y, width, height, frames, scale_x, scale_y):
        animation = []

        for i in range(frames):
            image = self.get_image(x + (i * width), y, width, height)
            image = pg.transform.scale(image, (scale_x, scale_y))
            animation.append(image)

        return animation
