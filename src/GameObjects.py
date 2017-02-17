import pygame as pg
import numpy as np
from GameAssets import *

class GameObject():
    """
    """

    def __init__(self, args):
        '''
        '''
        self.rect = np.array(args[0:4])
        self.vel = np.array([0.,0.])
        self.acc = np.array([0.,0.])
        self.debug_color = (255, 255, 255)
        self.solid = False
        self.physics = False

    def update(self, delta, keys, game_data):
        '''
        '''
        self.rect[0] += self.vel[0] * delta
        self.rect[1] += self.vel[1] * delta

    def render(self, screen, game_data):
        '''
        '''
        draw_rect = self.rect.astype(int) + game_data.camera_pos.astype(int)
        if game_data.debug:
            pg.draw.rect(screen, self.debug_color, draw_rect.tolist(), 1)
            t = GameFonts.font_0.render(self.__class__.__name__, False, (255, 255, 255))
            screen.blit(t, (draw_rect[0] + (-t.get_width()/2 + draw_rect[2]/2), draw_rect[1] + (-t.get_height()/2  + draw_rect[3]/2)))

    def set_pos(self, x , y):
        '''
        '''
        self.rect[0] = x
        self.rect[1] = y

    def set_dim(self, w, l):
        '''
        '''
        self.rect[2] = w
        self.rect[3] = l

    def set_vel(self, vx, vy):
        '''
        '''
        self.vel[0] = vx
        self.vel[1] = vy

    def check_collision(self, rect):
        '''
        '''
        if (self.rect[0]+self.rect[2]<rect[0] or rect[0]+rect[2]<self.rect[0] or self.rect[1]+self.rect[3]<rect[1] or rect[1]+rect[3]<self.rect[1]): return False
        else: return True

class Player(GameObject):
    """
    """

    def __init__(self, args):
        '''
        '''
        super().__init__([args[0], args[1], 68.0, 116.0])
        self.solid = True
        self.physics = True
        self.debug_color = (0, 255, 0)
        self.animations =[
            SpriteSheet("../data/sprites/am2r_walk.png").get_animation(1, 9, 41, 36, 10, 123, 116),
            SpriteSheet("../data/sprites/am2r_walk.png").get_animation(3, 57, 41, 36, 10, 123, 116),
            SpriteSheet("../data/sprites/am2r_still.png").get_animation(198, 7, 41, 38, 1, 123, 116),
            SpriteSheet("../data/sprites/am2r_still.png").get_animation(242, 7, 41, 38, 1, 123, 116),
            SpriteSheet("../data/sprites/am2r_still.png").get_animation(110, 500, 41, 33, 1, 123, 99),
            SpriteSheet("../data/sprites/am2r_still.png").get_animation(70, 500, 41, 33, 1, 123, 99),
            SpriteSheet("../data/sprites/am2r_still.png").get_animation(159, 499, 41, 33, 1, 123, 99),
            SpriteSheet("../data/sprites/am2r_still.png").get_animation(200, 499, 41, 33, 1, 123, 99),
            ]
        self.anim_index = 2
        self.frame = 0
        self.secs = 0

    def update(self, delta, keys, game_data):
        '''
        '''
        limit = 150
        self.set_dim(68.0, 116.0)
        if keys[6] and self.on_ground(game_data) and self.acc[0] < 60: self.acc[0] *= 1.015
        if (not keys[6] or not self.on_ground(game_data) ) and self.acc[0] > 12.0: self.acc[0] -= 60
        if self.acc[0] < 12.0: self.acc[0] = 12.0
        if keys[0] and self.on_ground(game_data): self.vel[1] = -150
        if keys[1] and self.vel[0] > -limit:
            if self.on_ground(game_data): self.vel[0] -= self.acc[0]
            else: self.vel[0] -= 5
        if keys[2] and self.vel[0] < limit:
            if self.on_ground(game_data): self.vel[0] += self.acc[0]
            else: self.vel[0] += 5

        super().update(delta, keys, game_data)
        game_data.center_camera_on_game_object(self)

        if self.on_ground(game_data):
            if self.anim_index in [6, 7]: self.anim_index =  2
            if self.anim_index in [4, 5]: self.anim_index =  3

        if self.vel[0] > 10.0:
            self.anim_index = 1
            self.set_dim(75.0, 116.0)
        elif self.vel[0] > 0.0 : self.anim_index = 3
        if self.vel[0] < -10.0 :
            self.anim_index = 0
            self.set_dim(75.0, 116.0)
        elif self.vel[0] < 0.0: self.anim_index = 2

        if self.anim_index in [1,3] and not self.on_ground(game_data):
            if abs(self.vel[1]) > 1.0:
                self.anim_index = 6
                self.set_dim(75.0, 72.0)
            if self.vel[1] > -1.0:
                self.anim_index = 7
                self.set_dim(75.0, 83.0)
        if self.anim_index in [0,2] and not self.on_ground(game_data):
            if abs(self.vel[1]) > 1.0:
                self.anim_index = 4
                self.set_dim(68.0, 72.0)
            if self.vel[1] > -1.0:
                self.anim_index = 5
                self.set_dim(75.0, 83.0)

        self.secs += delta
        if self.secs > (1.25 - abs(self.vel[0]/limit)):
            self.secs = 0
            self.frame += 1
        if self.frame >= len(self.animations[self.anim_index]): self.frame = 0

    def render(self, screen, game_data):
        '''
        '''
        draw_rect = self.rect.astype(int) + game_data.camera_pos.astype(int)
        w = self.animations[self.anim_index][self.frame].get_width()
        h = self.animations[self.anim_index][self.frame].get_height()
        x_prime = draw_rect[0] + (draw_rect[2]/2.0) - (w/2.0)
        y_prime = draw_rect[1] + (draw_rect[3]/2.0) - (h/2.0)
        screen.blit(self.animations[self.anim_index][self.frame], (x_prime, y_prime))
        #super().render(screen, game_data)

    def on_ground(self, game_data):
        '''
        '''
        flag = False
        ground_objects = ['Wall', 'Platform']
        for i in ground_objects:
            for j in game_data.collisions[self]:
                if j.__class__.__name__ == i:
                    flag = True
                    return flag
        return flag

class Wall(GameObject):
    """
    """

    def __init__(self, args):
        '''
        '''
        super().__init__(args)
        self.solid = True
        self.bounce = args[4]
        self.friction = args[5]

    def update(self, delta, keys, game_data):
        '''
        '''
        tolerance = 0.0000000000001
        for go in game_data.collisions[self]:
            if go.solid and not issubclass(go.__class__, self.__class__) and not issubclass(self.__class__, go.__class__):
                if go.rect[0] >= self.rect[0]:
                    delta_x = self.rect[0] + self.rect[2] + tolerance - go.rect[0]
                elif go.rect[0] < self.rect[0]:
                    delta_x = -(go.rect[0] + go.rect[2] + tolerance - self.rect[0])
                if go.rect[1] >= self.rect[1]:
                    delta_y = self.rect[1] + self.rect[3] + tolerance - go.rect[1]
                elif go.rect[1] < self.rect[1]:
                    delta_y = -(go.rect[1] + go.rect[3] + tolerance - self.rect[1])
                if abs(delta_x) < abs(delta_y):
                    go.set_pos(go.rect[0] + delta_x, go.rect[1])
                    go.vel[0] = -go.vel[0] * (1 - self.bounce)
                else:
                    go.set_pos(go.rect[0], go.rect[1] + delta_y)
                    go.vel[1] = -go.vel[1] * (1 - self.bounce)
                    if delta_y < 0 and abs(go.vel[0]) < abs(self.vel[0]):
                        go.vel[0] += self.vel[0] * self.friction
                    else: go.vel[0] = go.vel[0] * (1 - self.friction)

        super().update(delta, keys, game_data)

    def set_bounce(self, b):
        '''
        '''
        self.bounce = b

    def set_friction(self, f):
        '''
        '''
        self.friction = f


class Platform(Wall):
    """
    """

    def __init__(self, args):
        '''
        '''
        super().__init__(args)
        self.speed = args[6]
        self.path_start = (self.rect[0], self.rect[1])
        self.path_end = (self.rect[0] + args[7][0], self.rect[1] + args[7][1])
        self.p_x = 1
        self.p_y = 1

    def update(self, delta, keys, game_data):
        '''
        '''
        if self.p_x == 1:
            if self.rect[0] < self.path_end[0]: self.vel[0] = self.speed
            else: self.p_x = not self.p_x
        else:
            if self.rect[0] > self.path_start[0]: self.vel[0] = -self.speed
            else: self.p_x   = not self.p_x
        if self.p_y == 1:
            if self.rect[1] < self.path_end[1]: self.vel[1] = self.speed
            else: self.p_y = not self.p_y
        else:
            if self.rect[1] > self.path_start[1]: self.vel[1] = -self.speed
            else: self.p_y  = not self.p_y
        super().update(delta, keys, game_data)


class GravityField(GameObject):
    """
    """

    def __init__(self, args):
        '''
        '''
        super().__init__(args)
        self.force_x = args[4]
        self.force_y = args[5]
        self.solid = False

    def update(self, delta, keys, game_data):
        '''
        '''
        for go in game_data.collisions[self]:
            if go.physics:
                go.vel[0] += self.force_x
                go.vel[1] += self.force_y
