import pygame
from scripts.player import Player
from scripts.tilemap import TileMap
from scripts.camera import Follow
import path
from scripts.assets import Assets
#from scripts.sfx import SoundMixer

import sys

# Current Development Time : 4H : 30 M



class Engine:
    
    def __init__(self) -> None:
        
        self.screen = pygame.display.set_mode((600, 400))
        self.display = pygame.Surface((300, 200))
        self.clock = pygame.time.Clock()
        pygame.mixer.init()

        self.assets = Assets().fetch(payload={'img' : {'all'}})

        
        
        self.tilemap = TileMap(self)
        self.tilemap.load(path.MAP_PATH + 'map.json')
        pos = self.tilemap.extract([('spawner', 1)], keep=False)[0]['pos']

        self.player = Player(self, pos=pos, size=(48, 60))
        self.follow = Follow('follow', 30)
        self.pos = [0, 0]

        # scale = (100, 100)

        # Fetch assets in data folders
        
        # assets = Assets()

        # assets.insert(
        #     {
        #         'moods' :{
        #                     'avatar/Neutral' : Animation(load_images('avatar/Neutral', scale=scale), dur=8, loop=True),
        #                     'avatar/Happy' : Animation(load_images('avatar/Happy', scale=scale), dur=8, loop=True),
        #                     'avatar/Frown' : Animation(load_images('avatar/Frown', scale=scale), dur=8, loop=True),
        #                     'avatar/Sad' : Animation(load_images('avatar/Sad', scale=scale), dur=8, loop=True),
        #                     'avatar/Angry' : Animation(load_images('avatar/Angry', scale=scale), dur=8, loop=True),
        #                     'cursor' : Animation(load_images('cursor'), dur=7, loop=True),
        #                 }
        #     },
        #     key='img'
        # )

        # assets.insert(
        #     {
        #         'mood_sfx' :{
        #                     'avatar/Neutral' : load_sounds('avatar/Neutral'),
        #                     'avatar/Happy' :  load_sounds('avatar/Happy'),
        #                     'avatar/Frown' : load_sounds('avatar/Frown'),
        #                     'avatar/Sad' : load_sounds('avatar/Sad'),
        #                     'avatar/Angry' : load_sounds('avatar/Angry'),
        #         }
        #     },
        #     key='sfx'
        # )

        #self.assets = assets.fetch(payload={'img' : ['all']})
        #self.sound = SoundMixer(assets.fetch(payload={'sfx' : ['all']}))
        #self.cursor = self.assets['cursor'].copy()

        #pygame.mouse.set_visible(False)
        pygame.init()


        self.font = pygame.font.Font(size=20)
    
    def run(self) -> None:
        movement = [0, 0]
        while True:
            
            self.display.fill((0, 0, 0))  
            mpos = list(pygame.mouse.get_pos())
            mpos = [mpos[0] // 2, mpos[1] // 2]

            render_scroll = self.follow.scroll(self.display, self.player.rect().center)

            pygame.draw.rect(self.display, (255, 255, 255), (0 - render_scroll[0], 0 - render_scroll[1], 20, 20))
            

            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        movement[0] = -1
                    if event.key == pygame.K_RIGHT:
                        movement[0] = 1
                    if event.key == pygame.K_DOWN:
                        pass
                    if event.key == pygame.K_UP:
                        self.player.velocity[1] = -5

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        movement[0] = 0
                    if event.key == pygame.K_RIGHT:
                        movement[0] = 0

            self.tilemap.render(self.display, offset=render_scroll)
            self.player.update(self.tilemap, self.display, movement=movement, offset=render_scroll)
            self.player.render(self.display, render_scroll)
            

        
            self.screen.blit(pygame.transform.scale(self.display, (self.screen.get_width(), self.screen.get_height())), (0, 0))

            # Clock capped at 60 fps            
            pygame.display.update()
            self.clock.tick(60)

Engine().run()