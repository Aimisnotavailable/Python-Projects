import random


def ramble():
    grid = []
    num_list = [i for i in range(1, 9)]
    for i in range(7):
        grid.append(random.choice(num_list))
        num_list.remove(grid[-1])
    grid.append(num_list[0])
    return grid
        

    
        