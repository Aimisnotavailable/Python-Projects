table = {
    "red_light": "stop",
    "green_light": "go",
    "yellow_light": "slow_down",
    "pedestrian_crossing": "stop",
    "emergency_vehicle": "yield"
}

class Agent:
    
    def __init__(self, table) -> None:
       self.table = table
    
    def lookup(self, percept) -> str:
        
        if percept in self.table:
            return self.table[percept]
        else:
            return 'default_action'
    
    def __str__(self) -> str:
        return f'Hi I am a table based agent'
    
    
agent = Agent(table)
action = ''

while action != 'default_action':
    percept = input('Enter a traffic condition : ').lower()

    action = agent.lookup(percept=percept)
    
    print(action)
    