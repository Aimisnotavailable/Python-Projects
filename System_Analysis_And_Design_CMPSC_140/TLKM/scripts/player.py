import pygame
from scripts.entities import NonobjEntities

class Player(NonobjEntities):

    def __init__(self, game, e_type='', pos=(0,0), size=(16,16)):
        self.parts = {'Head': '' , 'Torso' : '', 'Arms': '', 'Legs' : '', 'All' : ''}
        super().__init__(game, 'player', pos=pos, size=size)

        self.set_action('idle')

    # def render(self, surf, offset):
    #     pass

    def attack(self):
        pass

    def dash(self):
        pass

    def element(self):
        pass
