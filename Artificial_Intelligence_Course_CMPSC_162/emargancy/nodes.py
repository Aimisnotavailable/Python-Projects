import random
class Node:
    
    def __init__(self, name, pos=(100, 30)) -> None:
        self.name : str = name
        self.neighbours = {}
        self.pos = list(pos)
        
    def add_neighbour(self, neighbour, edge_name="" , weight={}) -> None:
        if neighbour.name not in self.neighbours:
            self.neighbours[neighbour.name] = [(neighbour, edge_name, weight)]
            neighbour.neighbours[self.name] = [(self, edge_name, weight)]
        else:
            self.neighbours[neighbour.name].append((neighbour, edge_name, weight))
            neighbour.neighbours[self.name].append((self, edge_name, weight))
        
        # neighbour.pos[0] += max(20, (weight['dist']) + 50 + 100 * -(0.1) if random.randint(0,1) else 0.1)
        # neighbour.pos[1] += max(20, (weight['dist']) + 50 + 100 * -(0.1) if random.randint(0,1) else 0.1)
            
    def add_neighbours(self, data=[]):
        for val in data:
            info = val.get_data()
            self.add_neighbour(info['neighbour'], info['e_name'], info['weights'])
        