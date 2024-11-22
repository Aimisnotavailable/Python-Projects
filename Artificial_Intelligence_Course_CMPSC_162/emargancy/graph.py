from nodes import Node

class Graph:
    
    def __init__(self, nodes=[]) -> None:
        self.nodes = {str(node) : Node(str(node)) for node in nodes}
    
    def make_graph(self):
        pass
    