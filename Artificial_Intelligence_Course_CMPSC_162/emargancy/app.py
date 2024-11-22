import pygame
import sys
import random

class App:
    
    def __init__(self):
        self.screen = pygame.display.set_mode((600, 400))
        self.display = pygame.Surface((300, 200))
        
        pygame.init()
        
        self.clock = pygame.Clock()
        
    def draw_nodes(self):
        for node in range(5):
            pygame.draw.circle(self.display, (random.random() * 255, random.random() * 255, random.random() * 255), (random.randint(10, 300), random.randint(10, 200)), 5)
    def run(self):
        
        while True:
            
            self.display.fill((255, 255, 0))
            
            self.draw_nodes()
            
            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.ext()
                    
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            
            self.clock.tick(60)
            pygame.display.update()

App().run()