class Node:
    
    def __init__(self, name) -> None:
        self.name = name
        self.neighbours = {}
        
    def add_neighbour(self, neighbour, edge_name="" , weight={}) -> None:
        if neighbour.name not in self.neighbours:
            self.neighbours[neighbour.name] = [(edge_name, weight)]
        else:
            self.neighbours[neighbour.name].append((edge_name, weight))
            
    def add_neighbours(self, data=[]):
        for val in data:
            info = val.get_data()
            self.add_neighbour(info['neighbour'], info['e_name'], info['weights'])
        