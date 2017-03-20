import pygame as pg
import numpy as np
from GameAssets import GameAssets as ga
import Transitions

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
        self.vel[0] += self.acc[0] * delta
        self.vel[1] += self.acc[1] * delta
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
            t = ga.font_0.render(self.__class__.__name__, False, self.debug_color)
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

    def on_ground(self, game_data, obj=[]):
        '''
        '''
        flag = False
        ground_objects = ['Wall', 'Floor', 'Lava_Pit'] + obj
        for i in ground_objects:
            for j in game_data.collisions[self]:
                if j.__class__.__name__ == i:
                    flag = True
                    return flag
        return flag

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
        self.active = True

    def update(self, delta, keys, game_data):
        '''
        '''
        if self.active:
            for go in game_data.collisions[self]:
                if go.physics:
                    go.acc[0] = self.force_x
                    go.acc[1] = self.force_y

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
            if game_data.player_pos[0] < self.get_pos()[0]:
                self.vel[0] = -50
            else:
                self.vel[0] = 50
        if self.on_ground(game_data):
            if game_data.player_pos[1] < self.get_pos()[1]:
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
        self.solid = False
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
        dim = game_data.screen_dim
        if ((draw_rect[2] > 160) or (draw_rect[3] > 160)):
            repeat_x = int(width/100)
            repeat_y = int(length/100)
            width = int(width/repeat_x)
            length = int(length/repeat_y)
            wall = pg.transform.scale(ga.wall, (width,  length))
            for i in range(0,repeat_x):
                for j in range(0,repeat_y):
                    if ((width*i)+draw_rect[0] + draw_rect[2] > 0 and (width*i)+draw_rect[0] < dim[0] and (length*j)+draw_rect[1] + draw_rect[3] > 0 and (length*j)+draw_rect[1] < dim[1]):
                        screen.blit(wall, ((width*i)+draw_rect[0], (length*j)+draw_rect[1]))
        else:
            wall = pg.transform.scale(ga.wall, (draw_rect[2],  draw_rect[3]))
            screen.blit(wall, (draw_rect[0], draw_rect[1]))
        super().render(screen, game_data)

class Floor(Wall):
    """
    """

    def __init__(self, args):
        '''
        '''
        super().__init__(args)

class Death_Pit(GameObject):
    """
    """

    def __init__(self, args):
        '''
        '''
        super().__init__(args)

    def update(self, delta, keys, game_data):
        '''
        '''
        for go in game_data.collisions[self]:
            if go.__class__.__name__ == 'Player':
                go.health = 0
        super().update(delta, keys, game_data)

class Game_Message(GameObject):
    """
    """

    def __init__(self, args):
        '''
        '''
        super().__init__(args[0:4])
        self.message = str(args[4])
        self.show = False

    def update(self, delta, keys, game_data):
        '''
        '''
        self.show = False
        for go in game_data.collisions[self]:
            if go.__class__.__name__ == 'Player':
                self.show = True

    def render(self, screen, game_data):
        '''
        '''
        if self.show:
            message = ga.font_3.render(self.message, False, (255 ,255 ,255))
            screen.blit(message, (game_data.screen_dim[0]/2.0 - (message.get_width()/2.0), 80))
        super().render(screen, game_data)

class Lava_Pit(Wall):
    """
    """

    def __init__(self, args):
        '''
        '''
        super().__init__(args)
        self.bounce = args[4]
        self.friction = args[5]
        self.debug_color = (255, 0, 0)

    def update(self, delta, keys, game_data):
        '''
        '''
        super().update(delta, keys, game_data)
        for go in game_data.collisions[self]:
            if go.__class__.__name__ == 'Player':
                go.health -= 0.1

    def render(self, screen, game_data):
        '''
        '''
        if not self.on_screen(game_data): return
        camera_pos = game_data.camera_pos.astype(int)
        draw_rect = self.rect.astype(int) + game_data.camera_pos.astype(int)

        width = draw_rect[2]
        length = draw_rect[3]
        dim = game_data.screen_dim
        if ((draw_rect[2] > 128) or (draw_rect[3] > 128)):
            repeat_x = int(width/127)
            repeat_y = int(length/100)
            width = (width/repeat_x) - 2
            length = length/repeat_y
            for i in range(int(camera_pos[0]/100),repeat_x+1):
                for j in range(int(camera_pos[1]/100),repeat_y):
                    if ((width*i)+draw_rect[0] + draw_rect[2] > 0 and (width*i)+draw_rect[0] < dim[0] and (length*j)+draw_rect[1] + draw_rect[3] > 0 and (length*j)+draw_rect[1] < dim[1]):
                        ga.lava.blit(screen, ((width*i)+draw_rect[0], (length*j)+draw_rect[1]))
        #super().render(screen, game_data)

class HitBox(GameObject):
    """
    """

    def __init__(self, args):
        '''
        '''
        super().__init__(args)
        self.debug_color = (255, 0, 0)
        self.direction = 0
        self.frame = 0

    def update(self, delta, keys, game_data):
        '''
        '''
        pass

    def render(self, screen, game_data):
        '''
        '''
        super().render(screen, game_data)


class Swing(HitBox):
    """
    """

    def __init__(self, args):
        '''
        '''
        super().__init__(args)

    def update(self, delta, keys, game_data):
        '''
        '''
        try:
            if self.frame > 4:
                for go in game_data.collisions[self]:
                    if go.solid and go.__class__.__name__ != 'Player':
                        if self.direction == 0:
                            if go.__class__.__name__ == 'Electric_Sheep' and self.frame == 5: go.health -= 40
                            go.vel[0] = 50
                            if go.__class__.__name__ == 'Crate': go.vel[0] = 100
                            go.rect[0] += 10
                            go.rect[1] -= 10
                            go.vel[1] = -100
                        elif self.direction == 1:
                            if go.__class__.__name__ == 'Electric_Sheep' and self.frame == 5: go.health -= 40
                            go.vel[0] = -50
                            if go.__class__.__name__ == 'Crate': go.vel[0] = -100
                            go.rect[0] -= 10
                            go.rect[1] -= 10
                            go.vel[1] = -100
            self.frame += 1
        except Exception as e:
            pass


class Bash(HitBox):
    """
    """

    def __init__(self, args):
        '''
        '''
        super().__init__(args)

    def update(self, delta, keys, game_data):
        '''
        '''
        try:
            if self.frame == 7:
                for go in game_data.collisions[self]:
                    if go.solid and go.__class__.__name__ != 'Player':
                        if self.direction == 0:
                            go.rect[1] -= 10
                            if go.__class__.__name__ == 'Electric_Sheep':
                                go.vel[0] = 100
                                go.health -= 25
                            go.vel[1] = 1000
                        elif self.direction == 1:
                            go.rect[1] -= 10
                            if go.__class__.__name__ == 'Electric_Sheep':
                                go.vel[0] = -100
                                go.health -= 25
                            go.vel[1] = 1000
            self.frame += 1
        except Exception as e:
            pass


class Shock(HitBox):
    """
    """

    def __init__(self, args):
        '''
        '''
        super().__init__(args)

    def update(self, delta, keys, game_data):
        '''
        '''
        try:
            if self.frame > 25:
                for go in game_data.collisions[self]:
                    if go.solid and go.__class__.__name__ != 'Electric_Sheep':
                        if self.direction == 0:
                            if go.__class__.__name__ == 'Player':
                                if not go.alive: continue
                                go.health -= 5
                            go.vel[0] = 100
                            go.rect[0] += 10
                            go.rect[1] -= 10
                            go.vel[1] = -100
                        elif self.direction == 1:
                            if go.__class__.__name__ == 'Player':
                                if not go.alive: continue
                                go.health -= 5
                            go.vel[0] = -100
                            go.rect[0] -= 10
                            go.rect[1] -= 10
                            go.vel[1] = -100
            self.frame += 1
        except Exception as e:
            pass

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
        self.attack_1 = False
        self.attack_2 = False
        self.hitbox = None

        self.health = 100.0
        self.alive = True

    def update(self, delta, keys, game_data):
        '''
        '''
        # Player Game Logic
        limit = 150
        speed = 10
        on_ground = self.on_ground(game_data, obj=['Crate','Teleporter'])

        game_data.player_health = self.health
        if self.alive and self.health <= 0:
            self.alive = False
            ga.smb_left_death.stop()
            ga.smb_right_death.stop()
            ga.smb_left_death.play()
            ga.smb_right_death.play()
            if self.last_delta[0] > 0: self.anim_index = 12
            else: self.anim_index = 13

        if not self.alive:
            if self.hitbox:
                game_data.remove_game_object(self.hitbox)
                self.hitbox = None
            if ga.smb_left_death.isFinished() or ga.smb_right_death.isFinished():
                Transitions.run("fadeOut", 1.0)
                while(True):
                    if Transitions.updateScreen() == False: break
                    pg.display.flip()
                game_data.reset_level()
                return
            else:
                super().update(delta, keys, game_data)
                game_data.center_camera_on_game_object(self)
                return
        if keys[9] and on_ground: speed = 12
        if keys[0] and on_ground:
            ga.jump.play()
            ga.smb_left_jump.stop()
            ga.smb_right_jump.stop()
            ga.smb_left_jump.play()
            ga.smb_right_jump.play()
            self.vel[1] = -20 * speed
        if keys[4] and self.vel[0] > -limit:
            if on_ground: self.vel[0] -= speed
            else: self.vel[0] -= 7
        if keys[5] and self.vel[0] < limit:
            if on_ground: self.vel[0] += speed
            else: self.vel[0] += 7

        if keys[1] and not self.attack_1 and not self.attack_2:
            ga.swing.play()
            self.attack_1 = True
            ga.smb_left_swing.stop()
            ga.smb_right_swing.stop()
            ga.smb_left_swing.play()
            ga.smb_right_swing.play()

        if keys[11] and not self.attack_1 and not self.attack_2:
            ga.swing.play()
            self.attack_2 = True
            ga.smb_left_bash.stop()
            ga.smb_right_bash.stop()
            ga.smb_left_bash.play()
            ga.smb_right_bash.play()

        super().update(delta, keys, game_data)
        game_data.center_camera_on_game_object(self)
        game_data.player_pos = self.get_pos()

        if ga.smb_left_swing.isFinished() or ga.smb_right_swing.isFinished():
            self.attack_1 = False
            if self.hitbox and self.hitbox.__class__.__name__ == 'Swing':
                game_data.remove_game_object(self.hitbox)
                self.hitbox = None
        if ga.smb_left_bash.isFinished() or ga.smb_right_bash.isFinished():
            self.attack_2 = False
            if self.hitbox and self.hitbox.__class__.__name__ == 'Bash':
                game_data.remove_game_object(self.hitbox)
                self.hitbox = None

        # Animation Logic
        if self.last_delta[0] > 0:
            self.anim_index = 0
            if abs(self.vel[0]) > 10: self.anim_index = 2
            if not on_ground: self.anim_index = 4
            else:
                if self.last_delta[1] < -1: self.anim_index = 4
                if self.last_delta[1] > 1: self.anim_index = 7
            if self.attack_1:
                self.anim_index = 8
                if not self.hitbox:
                    self.hitbox = Swing([0, 0, 60, 70])
                    game_data.add_game_object(self.hitbox)
                self.hitbox.rect[0] = self.rect[0]+80
                self.hitbox.rect[1] = self.rect[1]+30
                self.hitbox.direction = 0
            if self.attack_2:
                self.anim_index = 10
                if not self.hitbox:
                    self.hitbox = Bash([0, 0, 60, 150])
                    game_data.add_game_object(self.hitbox)
                self.hitbox.rect[0] = self.rect[0]+80
                self.hitbox.rect[1] = self.rect[1]-15
                self.hitbox.direction = 0
        else:
            self.anim_index = 1
            if abs(self.vel[0]) > 10: self.anim_index = 3
            if not on_ground: self.anim_index = 5
            else:
                if self.last_delta[1] < -1: self.anim_index = 5
                if self.last_delta[1] > 1: self.anim_index = 6
            if self.attack_1:
                self.anim_index = 9
                if not self.hitbox:
                    self.hitbox = Swing([0, 0, 60, 70])
                    game_data.add_game_object(self.hitbox)
                self.hitbox.rect[0] = self.rect[0]-40
                self.hitbox.rect[1] = self.rect[1]+30
                self.hitbox.direction = 1
            if self.attack_2:
                self.anim_index = 11
                if not self.hitbox:
                    self.hitbox = Bash([0, 0, 60, 150])
                    game_data.add_game_object(self.hitbox)
                self.hitbox.rect[0] = self.rect[0]-40
                self.hitbox.rect[1] = self.rect[1]-15
                self.hitbox.direction = 1

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
        if self.anim_index == 10:
            x_prime = draw_rect[0] - 30
            y_prime = draw_rect[1] - 10
            ga.smb_left_bash.blit(screen, (x_prime, y_prime))
        if self.anim_index == 11:
            x_prime = draw_rect[0] - 65
            y_prime = draw_rect[1] - 10
            ga.smb_right_bash.blit(screen, (x_prime, y_prime))
        if self.anim_index == 12:
            x_prime = draw_rect[0] - 10
            y_prime = draw_rect[1] - 12
            ga.smb_left_death.blit(screen, (x_prime, y_prime))
        if self.anim_index == 13:
            x_prime = draw_rect[0]
            y_prime = draw_rect[1] - 12
            ga.smb_right_death.blit(screen, (x_prime, y_prime))
        super().render(screen, game_data)

class Electric_Sheep(GameObject):
    """
    """

    def __init__(self, args):
        '''
        '''
        super().__init__([args[0], args[1], 120, 100])
        self.solid = True
        self.physics = True
        self.debug_color = (0, 0, 255)
        self.anim_index = 0
        self.attack_1 = False
        self.hitbox = None
        self.health = 100
        self.alive = True
        self.agressiveness = args[2]

        self.attack_anim_0 = ga.es_right_shock.getCopy()
        self.attack_anim_1 = ga.es_left_shock.getCopy()

    def update(self, delta, keys, game_data):
        '''
        '''
        # Game Logic
        limit = 75
        on_ground = self.on_ground(game_data)
        action = np.random.randint(1000)
        player_pos = game_data.player_pos
        if abs(player_pos[0] - self.rect[0]) < game_data.screen_dim[0]*self.agressiveness:
            if player_pos[0] - self.rect[0] < 0: action = 1
            else: action = 2

        if self.alive and self.health < 0:
            self.alive = False
            ga.es_left_death.stop()
            ga.es_right_death.stop()
            ga.es_left_death.play()
            ga.es_right_death.play()
            if self.last_delta[0] > 0: self.anim_index = 2
            else: self.anim_index = 3

        if not self.alive:
            if ga.es_left_death.isFinished() or ga.es_right_death.isFinished():
                game_data.remove_game_object(self)
            if self.hitbox:
                game_data.remove_game_object(self.hitbox)
                self.hitbox = None
            return

        if action == 0 and on_ground:
            ga.jump.play()
            ga.es_left_jump.stop()
            ga.es_right_jump.stop()
            ga.es_left_jump.play()
            ga.es_right_jump.play()
            self.vel[1] = -150
        if not self.attack_1:
            if action%100 == 1 and self.vel[0] > -limit: self.vel[0] -= 10
            if action%100 == 2 and self.vel[0] < limit: self.vel[0] += 10
        if abs(player_pos[0]- self.rect[0]) < 200: action = 3
        if action%200 == 3 and not self.attack_1:
            self.attack_1 = True
            self.attack_anim_1.stop()
            self.attack_anim_0.stop()
            self.attack_anim_1.play()
            self.attack_anim_0.play()

        super().update(delta, keys, game_data)


        if self.attack_anim_1.isFinished() or self.attack_anim_0.isFinished():
            self.attack_1 = False
            if self.hitbox and self.hitbox.__class__.__name__ == 'Shock':
                game_data.remove_game_object(self.hitbox)
                self.hitbox = None

        # Animation Logic

        if self.last_delta[0] > 0:
            self.anim_index = 0
            if abs(self.vel[0]) > 10: self.anim_index = 4
            if not on_ground: self.anim_index = 4
            else:
                if self.last_delta[1] < -1: self.anim_index = 4
            if self.attack_1:
                self.anim_index = 6
                if not self.hitbox:
                    self.hitbox = Shock([0, 0, 140, 50])
                    game_data.add_game_object(self.hitbox)
                self.hitbox.rect[0] = self.rect[0]+110
                self.hitbox.rect[1] = self.rect[1]+15
                self.hitbox.direction = 0
        else:
            self.anim_index = 1
            if abs(self.vel[0]) > 10: self.anim_index = 5
            if not on_ground: self.anim_index = 5
            else:
                if self.last_delta[1] < -1: self.anim_index = 5
            if self.attack_1:
                self.anim_index = 7
                if not self.hitbox:
                    self.hitbox = Shock([0, 0, 140, 50])
                    game_data.add_game_object(self.hitbox)
                self.hitbox.rect[0] = self.rect[0]-120
                self.hitbox.rect[1] = self.rect[1]+15
                self.hitbox.direction = 1

    def render(self, screen, game_data):
        '''
        '''
        if not self.on_screen(game_data): return
        draw_rect = self.rect.astype(int) + game_data.camera_pos.astype(int)
        if self.anim_index == 0:
            x_prime = draw_rect[0] - 18
            y_prime = draw_rect[1] - 26
            ga.es_left_idle.blit(screen, (x_prime, y_prime))
        if self.anim_index == 1:
            x_prime = draw_rect[0] - 12
            y_prime = draw_rect[1] - 26
            ga.es_right_idle.blit(screen, (x_prime, y_prime))
        if self.anim_index == 2:
            x_prime = draw_rect[0] - 18
            y_prime = draw_rect[1] - 26
            ga.es_left_death.blit(screen, (x_prime, y_prime))
        if self.anim_index == 3:
            x_prime = draw_rect[0] - 12
            y_prime = draw_rect[1] - 26
            ga.es_right_death.blit(screen, (x_prime, y_prime))
        if self.anim_index == 4:
            x_prime = draw_rect[0] - 18
            y_prime = draw_rect[1] - 26
            ga.es_left_jump.blit(screen, (x_prime, y_prime))
        if self.anim_index == 5:
            x_prime = draw_rect[0] - 12
            y_prime = draw_rect[1] - 26
            ga.es_right_jump.blit(screen, (x_prime, y_prime))
        if self.anim_index == 6:
            x_prime = draw_rect[0] - 18
            y_prime = draw_rect[1] - 26
            self.attack_anim_1.blit(screen, (x_prime, y_prime))
        if self.anim_index == 7:
            x_prime = draw_rect[0] - 162
            y_prime = draw_rect[1] - 26
            self.attack_anim_0.blit(screen, (x_prime, y_prime))
        super().render(screen, game_data)


class Crate(GameObject):
    """
    """

    def __init__(self, args):
        '''
        '''
        super().__init__([args[0], args[1], 90, 90])
        self.solid = True
        self.physics = True
        self.debug_color = (0, 255, 255)

        self.mass = 1 - args[2]

    def update(self, delta, keys, game_data):
        '''
        '''
        # Game Logic
        tolerance = 0.0
        for go in game_data.collisions[self]:
            if go.solid:
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
                    self.vel[0] = go.vel[0] * self.mass
                else:
                    go.set_pos(go.rect[0], go.rect[1] + delta_y)
                    if not self.on_ground(game_data): self.vel[1] = go.vel[1] * self.mass
                    if delta_y < 0: go.vel[1] = 0
                    go.vel[0] = go.vel[0] * 0.75
                if go.__class__.__name__ == 'Crate': game_data.collisions[go].remove(self)
        super().update(delta, keys, game_data)

    def render(self, screen, game_data):
        '''
        '''
        if not self.on_screen(game_data): return
        draw_rect = self.rect.astype(int) + game_data.camera_pos.astype(int)
        screen.blit(ga.crate, (draw_rect[0], draw_rect[1]))
        super().render(screen, game_data)

class Teleporter(GameObject):
    """
    """

    def __init__(self, args):
        '''
        '''
        super().__init__([args[0], args[1], 100, 30])
        self.debug_color = (0, 0, 255)
        self.to_level = int(args[2])

    def update(self, delta, keys, game_data):
        '''
        '''
        # Game Logic
        tolerance = 0.0
        for go in game_data.collisions[self]:
            if go.__class__.__name__ == 'Player':
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
                    go.vel[0] = 0
                else:
                    go.set_pos(go.rect[0], go.rect[1] + delta_y)
                    go.vel[1] = 0
                    go.vel[0] = go.vel[0] * 0.75
                    Transitions.run("fadeOut", 1.5)
                    while(True):
                        if Transitions.updateScreen() == False: break
                        pg.display.flip()
                    game_data.switch_level(self.to_level)
                    return
        super().update(delta, keys, game_data)

    def render(self, screen, game_data):
        '''
        '''
        if not self.on_screen(game_data): return
        draw_rect = self.rect.astype(int) + game_data.camera_pos.astype(int)
        screen.blit(ga.teleporter, (draw_rect[0], draw_rect[1]-20))
        super().render(screen, game_data)
