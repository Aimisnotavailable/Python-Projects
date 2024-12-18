import pygame
from scripts.player import Player
from scripts.enemies import Enemy
from scripts.tilemap import TileMap
from scripts.camera import Follow
import path
from scripts.assets import Assets
#from scripts.sfx import SoundMixer

import sys

# Current Development Time : 4H : 30 M



class Engine:
    
    def __init__(self) -> None:
        
        self.screen = pygame.display.set_mode((1200, 800))
        self.display = pygame.Surface((600, 400))
        self.clock = pygame.time.Clock()
        pygame.mixer.init()

        self.assets = Assets().fetch(payload={'img' : {'all'}})

        # print(self.assets)
        
        self.background = self.assets['background']['all']
        self.tilemap = TileMap(self)
        self.tilemap.load(path.MAP_PATH + 'map.json')
        pos = self.tilemap.extract([('spawner', 1)], keep=False)[0]['pos']

        e_sp = self.tilemap.extract([('spawner', 0)], keep=False)

        self.enemy = Enemy(self, max_speed=4, pos=e_sp[0]['pos'], size=(110, 54))
        self.enemy1 = Enemy(self, e_type='enemy1', max_speed=4, pos=e_sp[1]['pos'], size=(110, 69))
        self.player = Player(self, max_speed=6, pos=pos, size=(64, 89))
        self.follow = Follow('follow', 20)
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

        self.combo = False
        self.font = pygame.font.Font(size=20)
        self.start = False
    
    def run(self) -> None:
        movement = [0, 0]
        while True:

            for event in pygame.event.get():
                    
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.player.running = -1
                        self.player.flip = True
                    if event.key == pygame.K_RIGHT:
                        self.player.running = 1
                        self.player.flip = False
                    if event.key == pygame.K_DOWN:
                        pass
                    if event.key == pygame.K_UP:
                        self.player.jump = True
                        self.player.velocity[1] = -5
                    if event.key == pygame.K_RETURN:
                        self.start = True

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.player.running = 0
                    if event.key == pygame.K_RIGHT:
                        self.player.running = 0
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if not self.player.attacking:
                            self.player.set_action('attack')
                            self.player.attack('normal_attack', self.player.combo)
                            self.player.attacking = True
                        elif not self.combo:
                            self.player.combo += 1
                            self.combo = True

            if self.start:
                self.display.fill((0, 0, 0))  
                mpos = list(pygame.mouse.get_pos())
                mpos = [mpos[0] // 2, mpos[1] // 2]

                render_scroll = self.follow.scroll(self.display, self.player.rect().center, offset=(0, 0))

                pygame.draw.rect(self.display, (255, 255, 255), (0 - render_scroll[0], 0 - render_scroll[1], 20, 20))

                pos = [0, 0]
                for i, background in enumerate(self.background):
                    background.render(self.display, (0, 0 - (self.background[i - 1].img.get_height() if i > 0 else 0)))
                #self.display.blit(self.a) 

                if self.enemy.rect().colliderect(self.player.rect()):
                    if self.player.attacking and not self.player.attacked:
                        self.enemy.hits += 1
                        self.enemy.attacked = 60 // self.enemy.hits
                        self.enemy.attacking = False
                    elif self.enemy.attacking and not self.enemy.attacked:
                        
                        self.player.attacked = 60
                        self.player.velocity = [-10 if self.enemy.flip else 10, -5]
            
                # print(self.enemy.velocity)
                if self.combo and self.player.animation.is_last_frame():
                    self.player.set_action('attack')
                    self.player.attack('normal_attack', self.player.combo)
                    self.combo = False

                self.tilemap.render(self.display, offset=render_scroll)
                self.player.update(self.tilemap, self.display, movement=movement, offset=render_scroll)
                self.player.render(self.display, render_scroll)

                self.enemy1.update(self.tilemap, self.display, offset=render_scroll)
                self.enemy1.render(self.display, render_scroll)
                self.enemy.update(self.tilemap, self.display, offset=render_scroll)
                self.enemy.render(self.display, render_scroll)
            else:
                self.display.blit(pygame.transform.scale(self.background[1].img, self.display.get_size()), (0, 0))
                self.display.blit(self.font.render('THE LOST KINGDOM', True, (0, 0, 0)), (100, 100))
                self.display.blit(self.font.render('MULAWIN', True, (0, 0, 0)), (200, 120))
                
        
            self.screen.blit(pygame.transform.scale(self.display, (self.screen.get_width(), self.screen.get_height())), (0, 0))

            # Clock capped at 60 fps            
            pygame.display.update()
            self.clock.tick(60)

Engine().run()