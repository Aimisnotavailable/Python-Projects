import pygame
from Scripts.Ai_scripts.utils import load_image, load_images, load_sound, load_sounds, Animation
from Scripts.Ai_scripts.assets import Assets
from Scripts.Ai_scripts.avatar import Avatar
from Scripts.Ai_scripts.sfx import SoundMixer
import sys

# Current Development Time : 4H : 30 M
    
class Engine:
    
    def __init__(self) -> None:
        
        self.screen = pygame.display.set_mode((600, 400))
        self.display = pygame.Surface((300, 200))
        self.clock = pygame.time.Clock()
        pygame.mixer.init()

        scale = (100, 100)

        # Fetch assets in data folders
        
        assets = Assets()

        assets.insert(
            {
                'moods' :{
                            'avatar/Neutral' : Animation(load_images('avatar/Neutral', scale=scale), dur=8, loop=True),
                            'avatar/Happy' : Animation(load_images('avatar/Happy', scale=scale), dur=8, loop=True),
                            'avatar/Frown' : Animation(load_images('avatar/Frown', scale=scale), dur=8, loop=True),
                            'avatar/Sad' : Animation(load_images('avatar/Sad', scale=scale), dur=8, loop=True),
                            'avatar/Angry' : Animation(load_images('avatar/Angry', scale=scale), dur=8, loop=True),
                            'cursor' : Animation(load_images('cursor'), dur=6, loop=True),
                        }
            },
            key='img'
        )

        assets.insert(
            {
                'mood_sfx' :{
                            'avatar/Neutral' : load_sounds('avatar/Neutral'),
                            'avatar/Happy' :  load_sounds('avatar/Happy'),
                            'avatar/Frown' : load_sounds('avatar/Frown'),
                            'avatar/Sad' : load_sounds('avatar/Sad'),
                            'avatar/Angry' : load_sounds('avatar/Angry'),
                }
            },
            key='sfx'
        )

        self.assets = assets.fetch(payload={'img' : ['all']})
        self.sound = SoundMixer(assets.fetch(payload={'sfx' : ['all']}))
        self.avatar = Avatar(self, size=scale)
        self.cursor = self.assets['cursor'].copy()

        pygame.mouse.set_visible(False)
        pygame.init()


        self.font = pygame.font.Font(size=20)
    
    def run(self) -> None:
        
        while True:
            
            self.display.fill((0, 0, 0))  
            mpos = list(pygame.mouse.get_pos())
            mpos = [mpos[0] // 2, mpos[1] // 2]

            # Mood Tooltips            
            self.display.blit(self.font.render(f'Current Mood : {self.avatar.current_mood}', True, (255, 255, 255)), (0, 0))
            self.display.blit(self.font.render(f'Action : {self.avatar.actions[self.avatar.current_mood]}', True, (255, 255, 255)), (0, 20))

            self.avatar.render(self.display)

            cursor_rect = self.cursor.img().get_rect(center=mpos)
            self.display.blit(self.cursor.img(), cursor_rect)
            
            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Updates the avatar based on the cursor position        
            update_mood = True

            if self.avatar.rect().collidepoint(mpos):
                update_mood = False
                self.cursor.update()
            else:
                self.cursor.frame = 0

            self.avatar.update(update_mood=update_mood)
                
            self.screen.blit(pygame.transform.scale(self.display, (self.screen.get_width(), self.screen.get_height())), (0, 0))

            # Clock capped at 60 fps            
            pygame.display.update()
            self.clock.tick(60)