import pygame
import os

# Old reused scripts
# See documentation at https://github.com/Aimisnotavailable/Python-Pygame

BASE_IMG_PATH = 'data/images/'
BASE_SFX_PATH = 'data/sounds/'

def load_image(path, scale=[], colorkey=(0,0,0)):
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey(colorkey)

    if scale:
        img = pygame.transform.scale(img, (img.get_width() * scale[0], img.get_height() * scale[1]))

    return img

def load_images(path, scale=[], colorkey=(0,0,0)):
    images = []

    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
        images.append(load_image(path + '/' + img_name, scale=scale, colorkey=colorkey))
    return images

def load_sound(path):
    sound = pygame.mixer.Sound(BASE_SFX_PATH + path)
    return sound

def load_sounds(path):
    sounds = []
    
    for sound_name in sorted(os.listdir(BASE_SFX_PATH + path)):
        sounds.append(load_sound(path + '/' + sound_name))
    return sounds

class Background:

    def __init__(self, img, depth):
        self.img = img
        self.depth = depth
    
    def render(self, surf, pos=(0, 0), offset=(0, 0)):
        surf.blit(pygame.transform.scale(self.img, surf.get_size()), (pos[0] - offset[0] * self.depth, pos[1] - offset[1] * self.depth))

class Animation:

    def __init__(self, images, dur=5, loop=True):
        self.images = images
        self.loop = loop
        self.image_duration = dur
        self.done = False
        self.frame = 0

    def copy(self):
        return Animation(self.images, self.image_duration, self.loop)
    
    def is_last_frame(self):
        if self.frame >= self.image_duration * len(self.images) - 2:
            return True
        return False
    def set_frame_to_last(self):
        self.frame = self.image_duration * len(self.images) -1 
         
    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.image_duration * len(self.images))
        else:
            self.frame = min(self.frame + 1, (self.image_duration * len(self.images)- 1))
            if self.frame >= self.image_duration * len(self.images) - 1:
                self.done = True
    
    def img(self):
        return self.images[int(self.frame / self.image_duration)]