import pygame

class Needle:

    def __init__(self, pos) -> None:
        self.pos = list(pos)
        self.disks = []
        self.size = (30, 100)
        self.img = pygame.Surface(self.size)
        pygame.draw.rect(self.img, (255, 255,255), (self.size[0] // 2, 0, self.size[0] // 10, self.size[1]))

    def rect(self) -> pygame.Rect:
        return self.img.get_rect(bottom=self.pos[1], centerx=self.pos[0])
    
    def add_disk(self, disk):
        self.disks.append(disk)
        sorted(self.disks, key=lambda x : -x.size[0])

    def remove_disk(self, disk):
        self.disks.remove(disk)

    def render(self, surf) -> None:
        surf.blit(self.img, self.rect())