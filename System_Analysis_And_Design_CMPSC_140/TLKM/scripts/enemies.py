from scripts.entities import NonobjEntities
import pygame
import random
import math

class Enemy(NonobjEntities):

    def __init__(self, game, e_type='enemy', pos=..., size=...):
        self.running = 0
        self.run_dur = 0
        super().__init__(game, 'enemy', pos, size)
        self.set_action('idle')

    def update(self, tilemap, surf, movement=(0,0), offset=(0,0)):
        if (random.random() * 999) < 12 and not self.run_dur:
            self.run_dur = 60
            self.running = random.choice([1, -1])

            if self.running < 0:
                self.flip = True
            else:
                self.flip = False
        
        if self.run_dur:
            self.set_action('run')
            p_loc = self.game.player.pos
            dist = math.sqrt(((p_loc[0] - self.pos[0]) ** 2) + ((p_loc[1] - self.pos[1]) ** 2))
        else:
            self.set_action('idle')
            self.running = 0
        
        self.run_dur = max(0, self.run_dur - 1)

        super().update(tilemap, surf, movement, offset)

        if not tilemap.solid_check((self.pos[0] + (0 if self.flip else self.size[0]) + (-20 if self.flip else 20), self.pos[1] + self.size[1] + 20)):
            self.running *= -1
        
        # pygame.draw.circle(surf, (255, 255, 255), (self.pos[0] + (0 if self.flip else self.size[0]) + (-20 if self.flip else 20) - offset[0], self.pos[1] + self.size[1] + 20 - offset[1]), 10)

        if self.collisions['right']:
            self.running = -1
        elif self.collisions['left']:
            self.running = 1