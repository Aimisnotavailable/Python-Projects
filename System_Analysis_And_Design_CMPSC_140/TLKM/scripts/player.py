import pygame
from scripts.entities import NonobjEntities

class Player(NonobjEntities):

    def __init__(self, game, e_type='', max_speed=0, pos=(0,0), size=(16,16)):
        self.attacking = False
        self.running = 0
        #self.parts = {'Head': '' , 'Torso' : '', 'Arms': '', 'Legs' : '', 'All' : ''}
        super().__init__(game, 'player',  max_speed, pos=pos, size=size)
        self.set_action('idle')

    # def render(self, surf, offset):
    #     pass
    def update(self, tilemap, surf, movement=(0,0), offset=(0,0)):
        super().update(tilemap, surf, movement, offset)
        
        if self.action == 'attack' and self.animation.done:
            self.attacking = False
            self.combo = 0

        if not self.attacking:
            if self.air_time > 4:
                if self.jump:
                    self.set_action('jump')
                else:
                    self.set_action('jump')
                    self.animation.set_frame_to_last()
            elif self.velocity[0] == 0:
                self.set_action('idle')
            elif self.running:
                self.set_action('run')

    # def attack(self):
    #     pass

    def dash(self):
        pass

    def element(self):
        pass
