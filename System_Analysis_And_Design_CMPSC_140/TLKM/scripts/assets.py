import pygame
from scripts.utils import load_image, load_images, load_sound, load_sounds, Animation
class Assets:

    def __init__(self):
        self.assets = {
           'img' : {
                     'tiles' :{
                                 'grass' : load_images('tiles/grass'),
                                 'test'  : load_images('tiles/test'),
                                 'test2'  : load_images('tiles/test2'),
                     },
                     'spawners' : {
                                 'spawner' : load_images('spawners'),
                     },
                     'entities' : {
                        'player' : {
                                    'idle' : {
                                       'all' : Animation(load_images('entities/player/idle', colorkey=(255, 0, 0)), dur=1.2),
                                    },
                                    'run' : {
                                       'all' : Animation(load_images('entities/player/run', colorkey=(255, 0, 0)), dur=2),
                                    },
                                    'attack':{
                                       'normal_attack' : [Animation(load_images('entities/player/attack/normal_attack/combo1', colorkey=(255, 0, 0)), dur=2, loop=False), 
                                                          Animation(load_images('entities/player/attack/normal_attack/combo2', colorkey=(255, 0, 0)), dur=2, loop=False),
                                                          Animation(load_images('entities/player/attack/normal_attack/combo3', colorkey=(255, 0, 0)), dur=2, loop=False)]
                                    }
                                 },
                        'enemy' : {
                                    'idle' : {
                                       'all' : Animation(load_images('entities/enemy/idle', scale=[1.4, 1.4], colorkey=(255, 0, 0)), dur=2),
                                    }
                        }
                     },
                     'backgrounds' : {
                        'background' : {
                                        'all' : load_images('background')
                        }
                     }
           },
           'sfx' : {
              
           }
        }

    def insert(self, assets, key=''):
       if key in self.assets:
          self.assets[key].update(assets)
          return True
       else:
          return False
       
    def fetch(self, payload={}, fetch_all=False):
        assets = {}
        if fetch_all:
          file_types = list(self.assets)
          for file_type in file_types:
              for obj_type in self.assets[file_type]:
                assets.update(self.assets[file_type][obj_type])
          return assets
        else:
          for file_type in payload:
            if 'all' in payload[file_type]:
               for obj_type in self.assets[file_type]:
                  assets.update(self.assets[file_type][obj_type])
            else:
              for obj_type in payload[file_type]:
                assets.update(self.assets[file_type][obj_type])
          return assets 
        