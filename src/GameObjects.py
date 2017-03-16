import pygame as pg
import numpy as np
from GameAssets import GameAssets as ga
from GameAssets import GameAssets as gf

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

        self.last_delta = np.array([0., 0.])

    def update(self, delta, keys, game_data):
        '''
        '''
        self.last_delta[0] = self.vel[0] * delta
        self.last_delta[1] = self.vel[1] * delta
        self.rect[0] += self.last_delta[0]
        self.rect[1] += self.last_delta[1]

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

    def get_pos(self):
        '''
        '''
        return [self.rect[0], self.rect[1]]

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

    def on_screen(self, game_data):
        '''
        '''
        draw_rect = self.rect.astype(int) + game_data.camera_pos.astype(int)
        dim = game_data.screen_dim
        return (draw_rect[0] + draw_rect[2] > 0 and draw_rect[0] < dim[0] and draw_rect[1] + draw_rect[3] > 0 and draw_rect[1] < dim[1])

class Player(GameObject):
    """
    """

    def __init__(self, args):
        '''
        '''
        super().__init__([args[0], args[1], 100, 115])
        self.solid = True
        self.physics = True
        self.debug_color = (0, 255, 0)
        self.anim_index = 0
        self.attacking = False

    def update(self, delta, keys, game_data):
        '''
        '''
        # Player Game Logic
        limit = 150
        on_ground = self.on_ground(game_data)
        if keys[9] and on_ground and self.acc[0] < 20: self.acc[0] *= 1.015
        if (not keys[9] or not on_ground) and self.acc[0] > 12.0: self.acc[0] -= 60
        if self.acc[0] < 12.0: self.acc[0] = 12.0
        if keys[0] and on_ground:
            ga.smb_left_jump.stop()
            ga.smb_right_jump.stop()
            ga.smb_left_jump.play()
            ga.smb_right_jump.play()
            self.vel[1] = -150
        if keys[4] and self.vel[0] > -limit:
            if on_ground: self.vel[0] -= self.acc[0]
            else: self.vel[0] -= 5
        if keys[5] and self.vel[0] < limit:
            if on_ground: self.vel[0] += self.acc[0]
            else: self.vel[0] += 5

        if keys[1]:
            self.attacking = True
            ga.smb_left_swing.stop()
            ga.smb_right_swing.stop()
            ga.smb_left_swing.play()
            ga.smb_right_swing.play()

        super().update(delta, keys, game_data)
        game_data.center_camera_on_game_object(self)
        Player.position = self.get_pos()

        if ga.smb_left_swing.isFinished() or ga.smb_right_swing.isFinished(): self.attacking = False

        # Animation Logic
        if self.last_delta[0] > 0:
            self.anim_index = 0
            if abs(self.vel[0]) > 10: self.anim_index = 2
            if not on_ground: self.anim_index = 4
            else:
                if self.last_delta[1] < -1: self.anim_index = 4
                if self.last_delta[1] > 1: self.anim_index = 7
            if self.attacking: self.anim_index = 8
        else:
            self.anim_index = 1
            if abs(self.vel[0]) > 10: self.anim_index = 3
            if not on_ground: self.anim_index = 5
            else:
                if self.last_delta[1] < -1: self.anim_index = 5
                if self.last_delta[1] > 1: self.anim_index = 6
            if self.attacking: self.anim_index = 9

    def render(self, screen, game_data):
        '''
        '''
        draw_rect = self.rect.astype(int) + game_data.camera_pos.astype(int)
        if self.anim_index == 0:
            x_prime = draw_rect[0] - 10
            y_prime = draw_rect[1] - 12
            ga.smb_left_idle.blit(screen, (x_prime, y_prime))
        if self.anim_index == 1:
            x_prime = draw_rect[0]
            y_prime = draw_rect[1] - 12
            ga.smb_right_idle.blit(screen, (x_prime, y_prime))
        if self.anim_index == 2:
            x_prime = draw_rect[0] - 10
            y_prime = draw_rect[1] - 10
            ga.smb_left_run.blit(screen, (x_prime, y_prime))
        if self.anim_index == 3:
            x_prime = draw_rect[0]
            y_prime = draw_rect[1] - 10
            ga.smb_right_run.blit(screen, (x_prime, y_prime))
        if self.anim_index == 4:
            x_prime = draw_rect[0] - 10
            y_prime = draw_rect[1] - 10
            ga.smb_left_jump.blit(screen, (x_prime, y_prime))
        if self.anim_index == 5:
            x_prime = draw_rect[0]
            y_prime = draw_rect[1] - 10
            ga.smb_right_jump.blit(screen, (x_prime, y_prime))
        if self.anim_index == 6:
            x_prime = draw_rect[0] - 10
            y_prime = draw_rect[1] - 10
            ga.smb_left_hang.blit(screen, (x_prime, y_prime))
        if self.anim_index == 7:
            x_prime = draw_rect[0]
            y_prime = draw_rect[1] - 10
            ga.smb_right_hang.blit(screen, (x_prime, y_prime))
        if self.anim_index == 8:
            x_prime = draw_rect[0] - 30
            y_prime = draw_rect[1] - 10
            ga.smb_left_swing.blit(screen, (x_prime, y_prime))
        if self.anim_index == 9:
            x_prime = draw_rect[0] - 65
            y_prime = draw_rect[1] - 10
            ga.smb_right_swing.blit(screen, (x_prime, y_prime))
        super().render(screen, game_data)

    def on_ground(self, game_data):
        '''
        '''
        flag = False
        ground_objects = ['Wall', 'Floor']
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
        if self.on_ground(game_data):
            if Player.position[0] < self.get_pos()[0]:
                self.vel[0] = -50
            else:
                self.vel[0] = 50
        if self.on_ground(game_data):
            if Player.position[1] < self.get_pos()[1]:
                self.vel[1] = -50
            else:
                self.vel[1] = 50

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
        ground_objects = ['Wall', 'Floor']
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
                    go.vel[1] = go.vel[1] * (1 - self.friction * 0.5)
                else:
                    go.set_pos(go.rect[0], go.rect[1] + delta_y)
                    go.vel[1] = -go.vel[1] * (1 - self.bounce)
                    go.vel[0] = go.vel[0] * (1 - self.friction)

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
        if not self.on_screen(game_data): return
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
        super().render(screen, game_data)

class Floor(GameObject):
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
                    go.vel[0] = go.vel[0] * (1 - self.friction)

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
        if not self.on_screen(game_data): return
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
        super().render(screen, game_data)

class Lava_Pit(GameObject):
    """
    """

    def __init__(self, args):
        '''
        '''
        super().__init__(args)
        self.solid = True
        self.bounce = args[4]
        self.friction = args[5]
        self.lava = ga.lava
        self.anim_speed = 4

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
        if not self.on_screen(game_data): return
        draw_rect = self.rect.astype(int) + game_data.camera_pos.astype(int)
        anim = ga.animate(self.lava, self.anim_speed, game_data.delta_sum)

        width = draw_rect[2]
        length = draw_rect[3]
        if ((draw_rect[2] > 160) or (draw_rect[3] > 160)):
            repeat_x = int(width/100)
            repeat_y = int(length/100)
            width = int(width/repeat_x)
            length = int(length/repeat_y)
            anim = pg.transform.scale(anim, (width,  length))
            for i in range(0,repeat_x):
                for j in range(0,repeat_y):
                    screen.blit(anim, ((width*i)+draw_rect[0], (length*j)+draw_rect[1]))
        else:
            anim = pg.transform.scale(self.wall_img, (draw_rect[2],  draw_rect[3]))
            screen.blit(anim, (draw_rect[0], draw_rect[1]))
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
