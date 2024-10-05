import pygame
from Scripts.utils import load_image, load_images, load_sound, load_sounds, Animation
from Scripts.assets import Assets
from Scripts.blocks import Blocks
from Scripts.rambler import ramble
import sys
import random

# Current Development Time : 4H : 30 M
    
class Engine:
    
    def __init__(self) -> None:
        
        self.screen = pygame.display.set_mode((600, 400))
        self.display = pygame.Surface((300, 200))
        self.clock = pygame.time.Clock()
        pygame.mixer.init()


        # Fetch assets in data folders
        
        assets = Assets()

        assets.insert(
            {
                'smear' : {

                    'smear' : Animation(load_images('smear'), dur=5, loop=True)
                }
            },
            key='img'
        )

        self.assets = assets.fetch(payload={'img' : ['all']})

        center =(self.display.get_width() // 2, self.display.get_height() // 2)

        print(self.assets)

        #self.sound = SoundMixer(assets.fetch(payload={'sfx' : ['all']}))
        #self.avatar = Avatar(self, size=scale)
        #self.cursor = self.assets['cursor'].copy()

        #pygame.mouse.set_visible(False)
        pygame.init()

        self.font = pygame.font.Font(size=20)
        self.goal_font = pygame.font.Font(size=10)
        self.blocks = [Blocks(num, self.font, grid_pos=(i%3, i//3), center=center, color=[min(255, max(5, (random.random() + 0.3) * 255)) for c in range(3)]) for num, i in zip(ramble(), range(1, 9))]
        self.goal =[Blocks(num, self.goal_font, grid_pos=(i%3, i//3), center=(10, 10), color=[min(255, max(5, (random.random() + 0.3) * 255)) for c in range(3)], size=(10, 10)) for num, i in zip(ramble(), range(1, 9))]
        self.blank_pos = [0, 0]
        
        print(self.blocks)
    
    def run(self) -> None:
        
        while True:
            
            self.display.fill((0, 0, 0))  
            mpos = list(pygame.mouse.get_pos())
            mpos = [mpos[0] // 2, mpos[1] // 2]

            self.display.blit(self.assets['smear'].img(), mpos)
            self.assets['smear'].update()

            for block, goal in zip(self.blocks, self.goal):
                block.update()
                block.render(self.display)
                goal.render(self.display)
            # # Mood Tooltips            
            # self.display.blit(self.font.render(f'Current Mood : {self.avatar.current_mood}', True, (255, 255, 255)), (0, 0))
            # self.display.blit(self.font.render(f'Action : {self.avatar.actions[self.avatar.current_mood]}', True, (255, 255, 255)), (0, 20))

            # self.avatar.render(self.display)

            # cursor_rect = self.cursor.img().get_rect(center=mpos)
            # self.display.blit(self.cursor.img(), cursor_rect)
            
            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for block in self.blocks:
                            if block.rect().collidepoint(mpos):
                                self.blank_pos = block.move(self.blank_pos)

            # # Updates the avatar based on the cursor position        
            # update_mood = True

            # if self.avatar.rect().collidepoint(mpos):
            #     update_mood = False
            #     self.cursor.update()
            # else:
            #     self.cursor.frame = 0

            # self.avatar.update(update_mood=update_mood)
                
            self.screen.blit(pygame.transform.scale(self.display, (self.screen.get_width(), self.screen.get_height())), (0, 0))

            # Clock capped at 60 fps            
            pygame.display.update()
            self.clock.tick(60)

Engine().run()