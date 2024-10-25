import pygame

NEIGHBOUR_OFFSETS =[(0,1), (0, -1), (1, 0), (-1, 0)]

class Blocks:
    
    def __init__(self, num, font, grid_pos=(0, 0), center=(0, 0), color=(0, 0, 0), size=(30, 30)) -> None:
        self.grid_pos = list(grid_pos)
        self.color = color
        self.num = num
        self.size = size

        self.center = center
        self.pos = [self.grid_pos[0] * self.size[0] + self.center[0] - self.size[0], self.grid_pos[1] * self.size[1] + self.center[1] - self.size[1]]
        self.img = pygame.Surface(self.size)
        pygame.draw.rect(self.img, self.color, (0, 0, *self.size))
        pygame.draw.rect(self.img, (max(self.color[0] // 5, self.color[0] - 20), max(self.color[1] // 5, self.color[1] - 20), max(self.color[2] // 5, self.color[2] - 20)), (0, 0, *self.size), width=5)

        self.img.blit(font.render(str(self.num), True, (0, 0, 0)), (size[0]//2, size[1]//2))

    def rect(self) -> pygame.Rect:
        return pygame.Rect(*self.pos, *self.size)
    
    def move(self, game=None, blank_pos=[0, 0], ) -> list:
        for offset in NEIGHBOUR_OFFSETS:
            if self.grid_pos[0] + offset[0] == blank_pos[0] and self.grid_pos[1] + offset[1] == blank_pos[1]:
                self.grid_pos[0] += offset[0]
                self.grid_pos[1] += offset[1]
                game.sound.play('click', loop=0, vol=0.5)
                game.moves -=1 
                return [blank_pos[0] - offset[0], blank_pos[1] - offset[1]]
        return blank_pos

    def update(self) -> None:
        
        pos = [self.grid_pos[0] * self.size[0] + self.center[0] - self.size[0] - self.pos[0], self.grid_pos[1] * self.size[1] + self.center[1] - self.size[1] - self.pos[1]]
        if pos[0] != 0:
            self.pos[0] += 1 if pos[0] > 0 else -1
        elif pos[1] != 0:
            self.pos[1] += 1 if pos[1] > 0 else -1

    def render(self, surf) -> None:
        surf.blit(self.img, self.pos)