from scripts.entities import NonobjEntities
import pygame
import random
import math

class Enemy(NonobjEntities):

    def __init__(self, game, e_type='enemy',  max_speed=0, pos=..., size=...):
        self.running = 0
        self.run_dur = 0
        self.hits = 0
        self.in_range = 0
        self.path_finder = True
        self.aggro = True
        super().__init__(game, e_type, max_speed, pos, size)
        self.set_action('idle')

    def update(self, tilemap, surf, movement=(0,0), offset=(0,0)):

        if not tilemap.solid_check((self.pos[0] + (0 if self.flip else self.size[0]) + (-20 if self.flip else 20), self.pos[1] + self.size[1] + 20)):
            self.path_finder = False
        else:
            self.path_finder = True

        if not self.attacked:
            if (random.random() * 999) < 12 and not self.run_dur and not self.attacking:
                self.run_dur = 60
                self.running = random.choice([1, -1])

                if self.running < 0:
                    self.flip = True
                else:
                    self.flip = False
            
            p_loc = self.game.player.pos
            dist = math.sqrt(((p_loc[0] - self.pos[0]) ** 2) + ((p_loc[1] - self.pos[1]) ** 2))
            
            if self.path_finder:
                if dist < 200:
                    self.running = 1 if self.pos[0] < p_loc[0] else -1
                    self.run_dur = 30
                    if self.type == 'enemy':
                        if dist < 75:
                            self.in_range += 1
                            self.set_action('attack')
                            self.attack('normal_attack', combo=0)
                            self.attacking = True
                            self.just_attacked = False
                        else:
                            self.in_range = max(0, self.in_range-1)
                    
    
            if self.action == 'attack' and self.animation.done:
                self.attacking = False
                self.combo = 0

            if not self.attacking:
                if self.run_dur:
                    self.set_action('run')
                else:
                    self.set_action('idle')
                    self.running = 0
            
            self.run_dur = max(0, self.run_dur - 1)
            self.hits = 0
        else:
            self.set_action('attacked')
            self.running=0
            self.run_dur=0

        if not self.path_finder:
            self.running *= -1
                

        if self.collisions['right']:
            self.running = -1
        elif self.collisions['left']:
            self.running = 1

        super().update(tilemap, surf, movement, offset)

            
        # pygame.draw.circle(surf, (255, 255, 255), (self.pos[0] + (0 if self.flip else self.size[0]) + (-20 if self.flip else 20) - offset[0], self.pos[1] + self.size[1] + 20 - offset[1]), 10)

        