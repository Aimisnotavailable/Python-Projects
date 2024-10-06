import pygame
from Scripts.utils import load_image, load_images, load_sound, load_sounds, Animation
from Scripts.assets import Assets
from Scripts.blocks import Blocks
from Scripts.rambler import ramble
from Scripts.sfx import SoundMixer
import sys
import random

# Current Development Time : 3H : 00 M
    
class Engine:
    
    def __init__(self) -> None:
        
        self.screen = pygame.display.set_mode((600, 400))
        self.display = pygame.Surface((300, 200))
        self.clock = pygame.time.Clock()
        pygame.mixer.init()
        pygame.display.set_caption('8 Numba game')

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

        assets.insert(
            {
                'bgm' : {
                    'background_music' : load_sounds('bgm'),
                },
                'game_sfx' : {
                    'success' : load_sounds('success'),
                    'game_over' : load_sounds('game_over'),
                    'click' : load_sounds('click'),
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


        data = ramble()

        self.game_blocks = []
        self.goal_blocks = []
        self.blank_pos = []
        self.end_screen_dur = 0
        self.game_end = False
        self.game_end_color = (255, 0, 0)
        self.moves = random.randint(50, 100)
        
        self.sound.play('background_music')
        for i in range(len(data['nums'])):
            
            if data['nums'][i] != 0:
                color=[random.randint(40, 255) for i in range(3)]            
                self.game_blocks.append(Blocks(data['nums'][i], font=self.font, grid_pos=data['game_grid'][i], center=self.center, color=color))
                self.goal_blocks.append(Blocks(data['nums'][i], font=self.goal_font, grid_pos=data['goal_grid'][i], center=(10, 10), color=color, size=(10, 10)))
            else:
                self.blank_pos = data['game_grid'][i]

    def check(self) -> bool:
        for game, goal in zip(self.game_blocks, self.goal_blocks):
            if game.grid_pos != goal.grid_pos:
                return False
        return True
    
    def end_screen(self) -> None:
        for i in range(min(int(self.end_screen_dur), len(self.game_blocks))):
            pygame.draw.rect(self.display, (self.game_end_color), (*self.game_blocks[i].pos, *self.game_blocks[i].size), width=5)
        win = self.game_end_color == (255, 255, 255)

        if self.end_screen_dur == 0:
            self.sound.stop('background_music')
            self.sound.play('success' if win else 'game_over', loop=0)
        
        if self.end_screen_dur == 4:
            self.sound.play('background_music')

        text = 'Wow congratulations you did it!' if win else 'Try again maybe this time you\'ll win'
        self.display.blit(self.font.render("{} \n {:<5}Press ENTER to continue".format(text, "") , True, (255, 255, 255)), (30, self.center[1] + 60))

    def run(self) -> None:
        
        while True:
            
            self.display.fill((0, 0, 0))  
            mpos = list(pygame.mouse.get_pos())
            mpos = [mpos[0] // 2, mpos[1] // 2]

            # self.display.blit(self.assets['smear'].img(), mpos)
            # self.assets['smear'].update()

            self.display.blit(self.font.render(f'Beat the game with {self.moves} moves left', True, color=(255, 255, 255)), (40, self.center[1] - 60))
            for block, goal in zip(self.game_blocks, self.goal_blocks):
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
                    if not self.game_end:
                        if event.button == 1:
                            for block in self.game_blocks:
                                if block.rect().collidepoint(mpos):
                                    self.blank_pos = block.move(self, self.blank_pos)
                
                if event.type == pygame.KEYDOWN:
                    if not self.game_end:
                        if event.key == pygame.K_r:
                            self.game_end = True
                    elif int(self.end_screen_dur) >= len(self.game_blocks):
                        if event.key == pygame.K_RETURN:
                                self.sound.stop('background_music')
                                self.load()    

            if self.check():
                self.game_end = True
                self.game_end_color = (255, 255 ,255)
            elif self.moves <= 0:
                self.game_end = True

            if int(self.end_screen_dur) < len(self.game_blocks):
                if self.game_end:
                    self.end_screen()
                    self.end_screen_dur += 0.1
            else:
                self.end_screen()

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
