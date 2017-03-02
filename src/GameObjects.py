import pygame as pg
import numpy as np
from GameAssets import GameAnimations as ga
from GameAssets import GameFonts as gf

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
            t = gf.font_0.render(self.__class__.__name__, False, (255, 255, 255))
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
            ga.player_walk_left,
            ga.player_walk_right,
            ga.player_still_left,
            ga.player_still_right,
            ga.player_jump_left,
            ga.player_jump_right,
            ga.player_falling_left,
            ga.player_falling_right
            ]
        self.anim_index = 2
        self.anim_speed = 1

    def update(self, delta, keys, game_data):
        '''
        '''
        limit = 150
        self.set_dim(68.0, 116.0)
        if keys[9] and self.on_ground(game_data) and self.acc[0] < 20: self.acc[0] *= 1.015
        if (not keys[9] or not self.on_ground(game_data) ) and self.acc[0] > 12.0: self.acc[0] -= 60
        if self.acc[0] < 12.0: self.acc[0] = 12.0
        if keys[0] and self.on_ground(game_data): self.vel[1] = -150
        if keys[4] and self.vel[0] > -limit:
            if self.on_ground(game_data): self.vel[0] -= self.acc[0]
            else: self.vel[0] -= 5
        if keys[5] and self.vel[0] < limit:
            if self.on_ground(game_data): self.vel[0] += self.acc[0]
            else: self.vel[0] += 5

        super().update(delta, keys, game_data)
        game_data.center_camera_on_game_object(self)

        self.anim_speed = 5 - 2 * ((abs(self.vel[0]))/ limit)

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

    def render(self, screen, game_data):
        '''
        '''
        draw_rect = self.rect.astype(int) + game_data.camera_pos.astype(int)
        anim = ga.animate(self.animations[self.anim_index], self.anim_speed, game_data.delta_sum)
        w = anim.get_width()
        h = anim.get_height()
        x_prime = draw_rect[0] + (draw_rect[2]/2.0) - (w/2.0)
        y_prime = draw_rect[1] + (draw_rect[3]/2.0) - (h/2.0)
        screen.blit(anim, (x_prime, y_prime))
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
		
class Enemy_Dragon(GameObject):
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
            ga.dragon_fly_left,
            ga.dragon_fly_right,
            ga.dragon_still_left,
            ga.dragon_still_right,
            ga.dragon_fire_left,
            ga.dragon_fire_right,
            ga.dragon_die_left,
            ga.dragon_die_right
            ]
        self.anim_index = 2
        self.anim_speed = 1

    def update(self, delta, keys, game_data):
        '''
        '''
        limit = 150
        self.set_dim(68.0, 116.0)
        if self.on_ground(game_data) and self.acc[0] < 20: self.acc[0] *= 1.015
        if self.acc[0] < 12.0: self.acc[0] = 12.0
        if self.on_ground(game_data): self.vel[1] = -150
        if self.vel[0] < limit:
            if self.on_ground(game_data): self.vel[0] += self.acc[0]
            else: self.vel[0] += 1

        super().update(delta, keys, game_data)

        self.anim_speed = 13

        if self.on_ground(game_data):
            if self.anim_index in [6, 7]: self.anim_index =  2
            if self.anim_index in [4, 5]: self.anim_index =  3

        if self.vel[0] > 10.0:
            self.anim_index = 1
        if self.vel[0] < -10.0 :
            self.anim_index = 0


    def render(self, screen, game_data):
        '''
        '''
        draw_rect = self.rect.astype(int) + game_data.camera_pos.astype(int)
        anim = ga.animate(self.animations[self.anim_index], self.anim_speed, game_data.delta_sum)
        w = anim.get_width()
        h = anim.get_height()
        x_prime = draw_rect[0] + (draw_rect[2]/2.0) - (w/2.0)
        y_prime = draw_rect[1] + (draw_rect[3]/2.0) - (h/2.0)
        screen.blit(anim, (x_prime, y_prime))
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
        self.wall_img = pg.image.load('../data/sprites/metal_block.png').convert()

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

    def render(self, screen, game_data):
        '''
        '''
        draw_rect = self.rect.astype(int) + game_data.camera_pos.astype(int)
        width = draw_rect[2]
        length = draw_rect[3]
        if ((draw_rect[2] > 160) or (draw_rect[3] > 160)):
            repeat_x = int(width/100)
            repeat_y = int(length/100)
            width = int(width/repeat_x)
            length = int(length/repeat_y)
            self.wall_img = pg.transform.scale(self.wall_img, (width,  length))
            for i in range(0,repeat_x):
                for j in range(0,repeat_y):
                    screen.blit(self.wall_img, ((width*i)+draw_rect[0], (length*j)+draw_rect[1]))
        else:
            self.wall_img = pg.transform.scale(self.wall_img, (draw_rect[2],  draw_rect[3]))
            screen.blit(self.wall_img, (draw_rect[0], draw_rect[1]))
        #super().render(screen, game_data)

class Platform(GameObject):
    """
    """

    def __init__(self, args):
        '''
        '''
        super().__init__(args)
        self.solid = True
        self.bounce = args[4]
        self.friction = args[5]
        self.wall_img = pg.image.load('../data/sprites/light_floor.png').convert()

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

    def render(self, screen, game_data):
        '''
        '''
        draw_rect = self.rect.astype(int) + game_data.camera_pos.astype(int)
        width = draw_rect[2]
        length = draw_rect[3]
        if ((draw_rect[2] > 160) or (draw_rect[3] > 160)):
            repeat_x = int(width/100)
            repeat_y = int(length/100)
            width = int(width/repeat_x)
            length = int(length/repeat_y)
            self.wall_img = pg.transform.scale(self.wall_img, (width,  length))
            for i in range(0,repeat_x):
                for j in range(0,repeat_y):
                    screen.blit(self.wall_img, ((width*i)+draw_rect[0], (length*j)+draw_rect[1]))
        else:
            self.wall_img = pg.transform.scale(self.wall_img, (draw_rect[2],  draw_rect[3]))
            screen.blit(self.wall_img, (draw_rect[0], draw_rect[1]))
        #super().render(screen, game_data)


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
