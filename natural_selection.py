import random

class Agent:
    def __init__(self, x, y, environment):
        self.x = x
        self.y = y
        self.fitness = 0
        self.environment = environment
        self.death_rate = 0.01
        self.has_eaten = False

    def manhattan(self, food):
        return (abs(self.x - food[0]) + abs(self.y - food[1]))

    # Movement is completely random
    def move_randomly(self):
        self.x += random.randint(-1, 1)
        self.y += random.randint(-1, 1)
    
    # Movement to closest food object
    def move_to_food(self):
        closest = None
        dist = float('inf')

        # get closest food
        for i in range(len(self.environment.food_grid)):
            distance_to_food = self.manhattan(self.environment.food_grid[i])
            if distance_to_food < dist:
                closest = self.environment.food_grid[i]
                dist = distance_to_food
        
        # move to food if reasonable distance
        if dist <= 2:
            self.x = closest[0]
            self.y = closest[1]
        


    def eat(self):
        if ((self.x, self.y) in self.environment.food_grid):
            self.environment.food_grid.remove((self.x, self.y))
            self.has_eaten = True

    def calculate_fitness(self):
        # Calculate fitness based on distance from center of environment
        center_x = self.environment.width / 2
        center_y = self.environment.height / 2
        distance = ((self.x - center_x) ** 2 + (self.y - center_y) ** 2) ** 0.5
        if distance == 0:
            self.fitness = 0
        else:
            self.fitness = 1 / distance

    def die(self):
        self.environment.agents.remove(self)

class Environment:
    def __init__(self, width, height, num_agents, num_food):
        self.width = width
        self.height = height
        self.num_food = num_food
        self.agents = [Agent(random.randint(0, width), random.randint(0, height), self) for _ in range(num_agents)] # 10 agents to start
        self.agent_counts = [len(self.agents)]
        self.food_grid = []
        self.remaining_food = []

    def populate_food(self):
        self.food_grid = [(random.randint(0, self.width), random.randint(0, self.height)) for _ in range(self.num_food)]

    def kill_the_hungry(self):
        self.agents = [agent for agent in self.agents if agent.has_eaten]

    def step(self):
        self.populate_food()
        for agent in self.agents:
            agent.has_eaten = False
            agent.move_to_food()
            agent.eat()
        
        self.kill_the_hungry()

        self.remaining_food.append(len(self.food_grid))

        # Select agents for reproduction based on food consumption
        new_agents = []
        for _ in range(len(self.agents)):
            parent = random.choice(self.agents)
            child_x = (parent.x)
            child_y = (parent.y)
            new_agents.append(Agent(child_x, child_y, self))
        self.agents = new_agents

        # Add current number of agents to list
        self.agent_counts.append(len(self.agents))

def simulate(iterations, num_agents=10, num_food=100) :
    env = Environment(100, 100, num_agents, num_food)
    for i in range(iterations) :
        print("Iteration Number " + str(i+1))
        print("Remaining Survivors: " + str(env.agent_counts[i]))
        env.step()
        
        if i == iterations - 1 :
            print(env.agent_counts)
            return(env.agent_counts, env.remaining_food)