from nodes import Node

class Graph:
    
    def __init__(self, nodes=[]) -> None:
        self.nodes = {str(node) : Node(str(node)) for node in nodes}
    
    def make_graph(self, neighbour_list) -> dict[str : Node]:
        for neighbour in neighbour_list:
            for key, val in neighbour.items():
                self.nodes[key].add_neighbours(val)
        #return self.nodes
    
    def find_path(self, start : Node, end : Node, cond=""):
        stack : list = [[start, 0, []]]
        data : dict[Node : dict]
        visited = set()
        
        while stack:
            curr, weight, curr_path = stack.pop(0)
            if curr == end:
                return [curr_path, weight]
            
            for key in curr.neighbours:
                for edge in curr.neighbours[key]:
                    if edge[0] not in visited:
                        visited.add(edge[0])
                        stack.append([edge[0], weight + edge[2][cond], curr_path + [edge[1]]])
            
            sorted(stack, key=lambda x: x[2])    
            
            
            
            
    