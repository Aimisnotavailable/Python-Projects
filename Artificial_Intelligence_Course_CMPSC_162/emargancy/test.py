from graph import Graph
from neighbour import Neighbour_data
import random 
barangays = [
    "Brgy. 1, Sta. Rita (Pob.)", "Brgy. 2, San Andres I (Pob.)", "Brgy. 3, San Andres II (Pob.)",
    "Brgy. 4, San Simon I (Pob.)", "Brgy. 5, San Simon II (Pob.)", "Brgy. 6, San Pedro I (Pob.)",
    "Brgy. 7, San Pedro II (Pob.)", "Brgy. 8, San Agustin I (Pob.)", "Brgy. 9, San Agustin II (Pob.)",
    "Brgy. 10, San Vicente (Pob.)", "Brgy. 11, Sta. Filomena I (Pob.)", "Brgy. 12, Sta. Filomena II (Pob.)",
    "Brgy. 13, San Gabriel I (Pob.)", "Brgy. 14, San Gabriel II (Pob.)", "Brgy. 15, San Roque I (Pob.)",
    "Brgy. 16, San Roque II (Pob.)", "Brgy. 17, Sto. Cristo I (Pob.)", "Brgy. 18, Sto. Cristo II (Pob.)",
    "Brgy. 19, Nambaran", "Brgy. 19-A, Tambidao", "Brgy. 20, Pulangi", "Brgy. 21, Libtong",
    "Brgy. 22, Bani", "Brgy. 23, Paninaan", "Brgy. 24, Macupit", "Brgy. 25, Tubburan",
    "Brgy. 26, Teppang", "Brgy. 27, Duripes", "Brgy. 27-A, Pungto", "Brgy. 28, Cabusligan",
    "Brgy. 29, Pasngal", "Brgy. 30, Cadaratan", "Brgy. 31, Calioet-Libong", "Brgy. 32, Corocor",
    "Brgy. 33, Cabulalaan", "Brgy. 34, Cabaruan", "Brgy. 35, Pipias", "Brgy. 36, Natba",
    "Brgy. 37, Ganagan", "Brgy. 37-A, Casilian", "Brgy. 38, Sangil", "Brgy. 39, Pasiocan", "Brgy. 40, Buyon"
]

graph = Graph(barangays)
neighbour_list = [{}]

for barangay in barangays:
  curr = barangay
  temp = barangays.copy()
  temp.remove(curr)
  for i in range(20):
    generate_b = graph.nodes[random.choice(temp)]
    temp.remove(generate_b.name)
    neighbour_list[0].update({barangay : [Neighbour_data(generate_b, ''.join([chr(random.randint(48, 122)) for i in range(10)]), {'dist' : random.randint(300, 1000),'cost' : random.randint(30, 40),'time' : random.randint(150, 1500)})]}) 

graph.make_graph(neighbour_list) 
graph.find_path(graph.nodes[random.choice(barangays)], graph.nodes[random.choice(barangays)], "dist")

