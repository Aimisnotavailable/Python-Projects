class Neighbour_data:
    
    def __init__(self, neighbour, edge_name, weight={}) -> None:
        self.data = {"neighbour" : neighbour, "e_name" :edge_name, "weights" : weight}
    
    def get_data(self):
        return self.data