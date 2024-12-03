import pygame
import sys
import random
from graph import Graph
from nodes import Node
from neighbour import Neighbour_data

class App:
    
    def __init__(self):
        self.key_points = ['SM Downtown CDO', 'Limketkai Center', 'Discovery Hotel', 'USTP', 'Limketkai Luxe', 'Red Planet Hotel', 'Fire Station']
        self.graph = Graph(self.key_points)
        
        map = [{'SM Downtown CDO' : {Neighbour_data(self.graph.nodes['Discovery Hotel'], 'Claro Recto', {'dist' : 80, 'time' : 20}),
                                     Neighbour_data(self.graph.nodes['USTP'], 'Main Ave', {'dist' : 50, 'time' : 30}),
                                     Neighbour_data(self.graph.nodes['Red Planet Hotel'], 'Main Road', {'dist' : 20, 'time' : 5}),
                                     Neighbour_data(self.graph.nodes['Limketkai Luxe'], 'Ayala', {'dist' : 65, 'time' : 15}),
                                     Neighbour_data(self.graph.nodes['Limketkai Center'], 'Business Centers', {'dist' : 45, 'time' : 30})
                },
               'Limketkai Center' : {Neighbour_data(self.graph.nodes['USTP'], 'Flyover', {'dist' : 35, 'time' : 10})
                },
               'Discovery Hotel' : {Neighbour_data(self.graph.nodes['USTP'], "Robinson's Mall", {'dist' : 40, 'time' : 20})
                },
               'Fire Station' : {Neighbour_data(self.graph.nodes['SM Downtown CDO'], 'Main road', {'dist' : 90, 'time' : 30})}
            #    'USTP' : {
            #     },
            #    'Limketkai Luxe' : {
            #     },
            #    'Red Planet Hotel' : {
            #     },
               }]
        self.graph.make_graph(map)
        
        self.graph.nodes['SM Downtown CDO'].pos = (150, 100)
        self.graph.nodes['Limketkai Center'].pos = (150, 50)
        self.graph.nodes['Discovery Hotel'].pos = (100, 60)
        self.graph.nodes['USTP'].pos = (200, 170)
        self.graph.nodes['Limketkai Luxe'].pos = (75, 100)
        self.graph.nodes['Red Planet Hotel'].pos = (180, 120)
        self.graph.nodes['Fire Station'].pos = (5, 5)
        # for name, node in self.graph.nodes.items():
        #     print("NAME : ", name, " ", node.neighbours)
        # self.graph.find_path(self.graph.nodes['SM Downtown CDO'], self.graph.nodes['USTP'], 'dist')
        
        self.screen = pygame.display.set_mode((600, 400))
        self.display = pygame.Surface((300, 200))
        
        pygame.init()
        
        self.clock = pygame.Clock()
        
        self.selected = []
        self.mem = [self.graph.nodes['Fire Station']]
        self.find_mode = False
        
        self.font = pygame.font.Font(size=15)
    def draw_nodes(self):
        roads = set()
        for key, val in self.graph.nodes.items():
            pygame.draw.circle(self.display, (0, 255, 0) if self.graph.nodes[key] in self.mem else (0, 0, 255) if self.find_mode else (255, 255, 255), self.graph.nodes[key].pos, 5)
            for neighbour, vals in self.graph.nodes[key].neighbours.items():
                for inf in vals:
                    road = inf[1]
                    if road not in roads:
                        pygame.draw.line(self.display, (255, 255, 255) if road not in self.selected else (255, 0, 0), self.graph.nodes[key].pos, inf[0].pos)
                        roads.add(road)
                

    def run(self):
        
        while True:
            
            self.display.fill((0, 0, 0))
            
            self.draw_nodes()
            mpos = (pygame.mouse.get_pos()[0] // 2, pygame.mouse.get_pos()[1] // 2)
            
            self.display.blit(self.font.render(f"PRESS F TO START", True, (255, 255, 255)), (150, 0))
            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:
                        self.find_mode = not self.find_mode
                        self.selected = []
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for key, val in self.graph.nodes.items():
                            n_rect = pygame.Rect(*self.graph.nodes[key].pos, 7, 7)
                            n_rect.center = self.graph.nodes[key].pos
                            if n_rect.collidepoint(mpos):
                                if self.find_mode:
                                    if self.graph.nodes[key] not in self.mem:
                                        self.mem.append(self.graph.nodes[key])
                                        
                                        if len(self.mem) > 2:
                                            self.mem.pop(1)
            for key, val in self.graph.nodes.items():
                n_rect = pygame.Rect(*self.graph.nodes[key].pos, 7, 7)
                n_rect.center = self.graph.nodes[key].pos
                if n_rect.collidepoint(mpos):
                    inf_surf = pygame.Surface((max(60, 8 * (len(self.graph.nodes[key].name))), 15))
                    inf_surf.fill((255, 255, 255))
                    inf_surf.blit(self.font.render(f"Loc : {self.graph.nodes[key].name}", True, (0, 0, 0)), (0, 0))
                    self.display.blit(inf_surf, mpos)   
                                               
            if len(self.mem) == 2:
                self.selected, dist = self.graph.find_path(self.mem[0], self.mem[1], 'dist')
                self.display.blit(self.font.render(f"Path : {' -> '.join(self.selected)}", True, (255, 255, 255)), (0, 170))
                self.display.blit(self.font.render(f"Total distance : {dist}", True, (255, 255, 255)), (0, 180))
            if not self.find_mode:
                self.mem = [self.graph.nodes['Fire Station']]
                self.selected = []
                   
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            
            self.clock.tick(60)
            pygame.display.update()

App().run()