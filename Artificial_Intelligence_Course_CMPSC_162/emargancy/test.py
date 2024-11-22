from graph import Graph
from neighbour import Neighbour_data

names = ['A', 'B', 'C', 'D', 'E']

graph = Graph(names)

neighbour_list = [{'A' : [  Neighbour_data(graph.nodes['B'], 'test', {'dist' : 10, 'cost' : 20, 'dur' : 30}), 
                            Neighbour_data(graph.nodes['B'], 'test1', {'dist' : 11, 'cost' : 21, 'dur' : 32}),
                            Neighbour_data(graph.nodes['B'], 'test2', {'dist' : 12, 'cost' : 24, 'dur' : 33}),
                            Neighbour_data(graph.nodes['B'], 'test3', {'dist' : 13, 'cost' : 23, 'dur' : 34}),]},
                #   {'B' : ''},
                #   {'C' : ''},
                #   {'D' : ''},
                #   {'E' : ''},
                  ]
for neighbour in neighbour_list:
    for key, val in neighbour.items():
        graph.nodes[key].add_neighbours(val)
            
print(graph.nodes['A'].neighbours)