import pygame
import sys
import random
from graph import Graph
from nodes import Node
from neighbour import Neighbour_data

class App:
    
    def __init__(self):
        self.key_points = ['SM Downtown CDO', 'Limketkai Center', 'Discovery Hotel', 'USTP', 'Limketkai Luxe', 'Red Planet Hotel', 'Fire Station',]
        self.graph = Graph(self.key_points)
        
        map = [{'SM Downtown CDO' : {Neighbour_data(self.graph.nodes['Discovery Hotel'], 'Claro Recto', {'dist' : 80, 'time' : 20}),
                                     Neighbour_data(self.graph.nodes['USTP'], 'Main Ave', {'dist' : 50, 'time' : 30}),
                                     #
                                     Neighbour_data(self.graph.nodes['Limketkai Luxe'], 'Ayala', {'dist' : 65, 'time' : 15}),
                                     Neighbour_data(self.graph.nodes['Limketkai Center'], 'Business Centers', {'dist' : 45, 'time' : 30})
                },
               'Limketkai Center' : {Neighbour_data(self.graph.nodes['USTP'], 'Flyover', {'dist' : 35, 'time' : 10})
                },
               'Discovery Hotel' : {Neighbour_data(self.graph.nodes['USTP'], "Robinson's Mall", {'dist' : 40, 'time' : 20})
                },
               'Fire Station' : {Neighbour_data(self.graph.nodes['SM Downtown CDO'], 'Main Road', {'dist' : 90, 'time' : 30})},
               'USTP' : {
                                Neighbour_data(self.graph.nodes['Red Planet Hotel'], 'SM Road', {'dist' : 20, 'time' : 5}),
                },
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
        self.graph.nodes['Red Planet Hotel'].pos = (230, 120)
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
        
        self.scroll = [-145, -95]
        self.movement = [0, 0]
    def draw_nodes(self):
        roads = set()
        for key, val in self.graph.nodes.items():
            node = self.graph.nodes[key]
            pygame.draw.circle(self.display, (0, 255, 0) if node in self.mem else (0, 0, 255) if self.find_mode else (255, 255, 255), (node.pos[0] - self.scroll[0] , node.pos[1] - self.scroll[1]) , 5)
            for neighbour, vals in node.neighbours.items():
                for inf in vals:
                    road = inf[1]
                    if road not in roads:
                        pygame.draw.line(self.display, (255, 255, 255) if road not in self.selected else (255, 0, 0), (node.pos[0] - self.scroll[0] , node.pos[1] - self.scroll[1]), (inf[0].pos[0] - self.scroll[0] , inf[0].pos[1] - self.scroll[1]))
                        roads.add(road)
                

    def run(self):
        
        while True:
            
            self.display.fill((0, 0, 0))
            
            self.draw_nodes()
            mpos = (pygame.mouse.get_pos()[0] // 2, pygame.mouse.get_pos()[1] // 2)
            
            self.display.blit(self.font.render(f"PRESS F TO START", True, (255, 255, 255)), (100, 0))
            self.display.blit(self.font.render(f"USE ARROW KEYS TO MOVE", True, (255, 255, 255)), (100, 15))
            
            self.scroll = [self.scroll[0] + self.movement[0], self.scroll[1] + self.movement[1]]
            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:
                        self.find_mode = not self.find_mode
                        self.selected = []
                    
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = -1
                    if event.key == pygame.K_RIGHT:
                        self.movement[0] = 1
                    if event.key == pygame.K_DOWN:
                        self.movement[1] = 1
                    if event.key == pygame.K_UP:
                        self.movement[1] = -1
                        
                if event.type == pygame.KEYUP:
                    
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = 0
                    if event.key == pygame.K_RIGHT:
                        self.movement[0] = 0
                    if event.key == pygame.K_DOWN:
                        self.movement[1] = 0
                    if event.key == pygame.K_UP:
                        self.movement[1] = 0
                               
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for key, val in self.graph.nodes.items():
                            node = self.graph.nodes[key]
                            w_pos = node.pos[0] - self.scroll[0], node.pos[1] - self.scroll[1]
                            n_rect = pygame.Rect(*w_pos, 7, 7)
                            n_rect.center = w_pos
                            if n_rect.collidepoint(mpos):
                                if self.find_mode:
                                    if node not in self.mem:
                                        self.mem.append(node)
                                        
                                        if len(self.mem) > 2:
                                            self.mem.pop(1)
                                            
            for key, val in self.graph.nodes.items():
                node = self.graph.nodes[key]
                w_pos = node.pos[0] - self.scroll[0], node.pos[1] - self.scroll[1]
                n_rect = pygame.Rect(*w_pos, 7, 7)
                n_rect.center = w_pos
                if n_rect.collidepoint(mpos):
                    inf_surf = pygame.Surface((max(60, 8 * (len(node.name))), 15))
                    inf_surf.fill((255, 255, 255))
                    inf_surf.blit(self.font.render(f"Loc : {node.name}", True, (0, 0, 0)), (0, 0))
                    self.display.blit(inf_surf, mpos)   
                                               
            if len(self.mem) == 2:
                res = self.graph.find_path(self.mem[0], self.mem[1], 'dist')
                if res:
                    self.selected, dist = res
                    self.display.blit(self.font.render(f"Path : {' -> '.join(self.selected)}", True, (255, 255, 255)), (0, 170))
                    self.display.blit(self.font.render(f"Total distance : {dist}", True, (255, 255, 255)), (0, 180))
                else:
                    self.display.blit(self.font.render(f"NO PATH FOUND", True, (255, 255, 255)), (0, 170))
            if not self.find_mode:
                self.mem = [self.graph.nodes['Fire Station']]
                self.selected = []
                   
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            
            self.clock.tick(60)
            pygame.display.update()

App().run()