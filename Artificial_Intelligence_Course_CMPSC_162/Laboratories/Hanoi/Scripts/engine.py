import pygame
from Scripts.utils import load_image, load_images, load_sound, load_sounds, Animation
from Scripts.assets import Assets
from Scripts.sfx import SoundMixer
from Scripts.disk import Disk
from Scripts.needle import Needle
import sys
import random

# Current Development Time : 3H : 00 M
    
class Engine:
    
    def __init__(self) -> None:
        
        self.screen = pygame.display.set_mode((600, 400))
        self.display = pygame.Surface((300, 200))
        self.clock = pygame.time.Clock()
        pygame.mixer.init()
        pygame.display.set_caption('Hanoi')

        # Fetch assets in data folders
        
        assets = Assets()

        # assets.insert(
        #     {
        #         'smear' : {

        #             'smear' : Animation(load_images('smear'), dur=5, loop=True)
        #         }
        #     },
        #     key='img'
        # )

        assets.insert(
            {
                'bgm' : {
                    'background_music' : load_sounds('bgm'),
                },
                'game_sfx' : {
                    'success' : load_sounds('success'),
                },
            },
            key='sfx'
        )

        self.assets = assets.fetch(payload={'img' : ['all']})

        self.center =(self.display.get_width() // 2, self.display.get_height() // 2)


        #self.sound = SoundMixer(assets.fetch(payload={'sfx' : ['all']}))
        #self.avatar = Avatar(self, size=scale)
        #self.cursor = self.assets['cursor'].copy()

        #pygame.mouse.set_visible(False)
        pygame.init()

        self.sound = SoundMixer(assets.fetch(payload={'sfx' : ['all']}))
        self.font = pygame.font.Font(size=20)
        self.goal_font = pygame.font.Font(size=10)
        self.load()

    def load(self):
        
        self.board = []
        self.needles = []
        self.disks = []
        self.game_end = False

        for i in range(3):
            self.needles.append(Needle((50 + 100 * i, 175)))
        for i in range(4):
            self.disks.append(Disk((10, -20 * i), color=(min(1, (random.random() + 0.4)) * 255, min(1, (random.random() + 0.4)) * 255, min(1, (random.random() + 0.4)) * 255), size=(30 - 5 * i, 10), needle=self.needles[0]))
            self.needles[0].add_disk(self.disks[-1])

        self.sound.play('background_music')
        self.selected_disk = None

    def check(self): 
        if len(self.needles[-1].disks) == 4:
            self.sound.play('success', 0)
            return True
        return False
    
    def end_screen(self) -> None:
        win = self.game_end
        text = 'Wow congratulations you did it!' if win else 'Try again maybe this time you\'ll win'
        self.display.blit(self.font.render("{}".format(text) , True, (255, 255, 255)), (0, 0))
        self.display.blit(self.font.render("Press ENTER to continue".format(text) , True, (255, 255, 255)), (0, 20))

    def run(self) -> None:
        
        while True:
            self.display.fill((0, 0, 0))  
            mpos = list(pygame.mouse.get_pos())
            mpos = [mpos[0] // 2, mpos[1] // 2]

            # self.display.blit(self.assets['smear'].img(), mpos)
            # self.assets['smear'].update()

            # # Mood Tooltips            
            # self.display.blit(self.font.render(f'Current Mood : {self.avatar.current_mood}', True, (255, 255, 255)), (0, 0))
            # self.display.blit(self.font.render(f'Action : {self.avatar.actions[self.avatar.current_mood]}', True, (255, 255, 255)), (0, 20))

            # self.avatar.render(self.display)

            # cursor_rect = self.cursor.img().get_rect(center=mpos)
            # self.display.blit(self.cursor.img(), cursor_rect)

            self.game_end =  self.check()

            if self.game_end:
                self.end_screen()

            for needle in self.needles:
                needle.render(self.display)
            
            for disk in self.disks:
                disk.render(self.display)
                disk.update()

            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for needle in self.needles:
                            if needle.rect().collidepoint(mpos):
                                if needle.disks and not self.selected_disk:
                                    self.selected_disk = needle.disks[-1]
                                    needle.remove_disk(self.selected_disk)
                                    self.selected_disk.selected = True
                                else:
                                    if not needle.disks or self.selected_disk.size[0] < needle.disks[-1].size[0]:
                                        self.selected_disk.selected = False
                                        self.selected_disk.needle = needle
                                        needle.add_disk(self.selected_disk)
                                        self.selected_disk = None

                if event.type == pygame.KEYDOWN:
                    if self.game_end:
                        if event.key == pygame.K_RETURN:
                            self.load()
                            self.sound.stop('success')
                            self.sound.stop('background_music')
                                        
            
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