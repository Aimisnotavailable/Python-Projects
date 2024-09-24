import pygame
import os
BASE_IMG_PATH = 'data/images/'

# Old reused scripts
# See documentation at https://github.com/Aimisnotavailable/Python-Pygame

def load_image(path, scale=[]) -> pygame.image:
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey((0, 0, 0))
    
    if scale:
        img = pygame.transform.scale(img, scale)
    return img

def load_images(path, scale=[]) -> list[pygame.Surface]:
    images = []
    
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
        images.append(load_image(path + '/' + img_name, scale=scale))
        
    return images

class Animation:
    
    def __init__(self, imgs, dur, frame=0, loop=False) -> None:
        self.images = imgs
        self.dur = dur
        self.loop = loop
        self.frame = frame
        self.done = False
    
    def copy(self):
        return Animation(self.images, self.dur, loop=self.loop)
    
    def update(self) -> None:
        if self.loop:
            self.frame = (self.frame + 1) % (self.dur * len(self.images))
        else:
            self.frame = min(self.frame, (self.dur * len(self.images) - 1))
            if self.frame >= self.dur * (len(self.images) - 1):
                self.done = True
    
    def img(self) -> pygame.image:
        return self.images[int(self.frame/self.dur)]