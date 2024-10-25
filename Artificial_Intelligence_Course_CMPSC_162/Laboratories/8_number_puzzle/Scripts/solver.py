import copy
OFFSET = ((0, 1), (1, 0), (0, -1), (-1, 0))
class Solver:

    def __init__(self, blank, game, goal) -> None:
        self.blank_grid = blank.copy()
        self.start = game.copy()
        self.goal = goal
    
    def check(self, game, goal):
        for game_block, goal_block in zip(game, goal):
            if game_block != goal_block:
                return False
        return True
    
    def to_str(self, game) -> str:
        visited = ''
        for _ in game:
            for __ in _:
                visited += __
        return visited
    
    def solve(self) -> list:
        queue = [(self.start, list(self.blank_grid), [''], self.to_str(self.start), (0, 0))]
        states = set()
        #print(self.blank_grid)
        #print(queue)
        while queue:
            game, blank, path, s_val, move= queue.pop(0)

            if self.check(game, self.goal):
                return path
            states.add(s_val)
            #print(s_val)
            # FIX GAME HANDLING FOR MULTIPLE STATES
            for offset in OFFSET:
                adj = [blank[0] + offset[0], blank[1] + offset[1]]
                if adj[0] < 3 and adj[0] >= 0 and adj[1] < 3 and adj[1] >= 0:
                    n_game = copy.deepcopy(game)
                    temp = n_game[adj[0]][adj[1]]
                    n_game[adj[0]][adj[1]] = '0'
                    n_game[blank[0]][blank[1]] = temp
                    visited = self.to_str(n_game)
                    if visited not in states and (-(offset[0]) != move[0] or -(offset[1]) != move[1]): 
                        queue.append((n_game, adj, path + [str(temp)], visited, offset))
                    
        return []
    
