import random


def ramble(size=9, row=3, col=3) -> dict:
    grid_nums = []

    data = {
        'game_grid' : [],
        'goal_grid' : [],
        'nums'      : [],
    }

    num_list = [i for i in range(size)]

    for i in range(size - 1):
        grid_nums.append(random.choice(num_list))
        num_list.remove(grid_nums[-1])

    grid_nums.append(num_list[0])

    grid_pos = [(i, j) for i in range(row) for j in range(col)]
    grid_pos1 = grid_pos.copy()

    while grid_pos:
        temp = random.choice(grid_pos)
        temp1 = random.choice(grid_pos1)

        data['game_grid'].append(temp)
        data['goal_grid'].append(temp1)

        grid_pos.remove(temp)
        grid_pos1.remove(temp1)

    data['nums'] = grid_nums

    return data
        

    
        