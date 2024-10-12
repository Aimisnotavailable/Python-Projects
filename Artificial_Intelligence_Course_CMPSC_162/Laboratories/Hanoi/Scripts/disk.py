import pygame

class Disk:

    def __init__(self, pos, color, size, needle) -> None:
        self.pos = list(pos)
        self.size = size
        self.color = color

        self.needle = needle
        self.img = pygame.Surface(size)
        self.img.fill(color)
        self.selected = False
        self.velocity = 0

    def rect(self) -> pygame.Rect:
        return pygame.Rect(*self.pos, *self.size)
    
    def update(self) -> None:
        self.pos[0] = self.needle.rect().centerx - (self.size[0] - self.needle.size[0]//10) // 2

        if self.selected:
            self.pos[1] = self.needle.rect().top - 50
            return
        
        self.multip = 1

        for i in range(len(self.needle.disks)):
            if self.needle.disks[i] == self:
                self.multip = i + 1

        self.pos[1] = min(self.needle.rect().bottom - self.size[1] * self.multip, self.pos[1] + self.velocity)
        self.velocity = min(5, self.velocity + 0.2) if not self.selected else 0
            
    def render(self, surf) -> None:
        surf.blit(self.img, self.pos)