import random

class Agent:
    def __init__(self, x, y, environment):
        self.x = x
        self.y = y
        self.fitness = 0
        self.environment = environment
        self.death_rate = 0.01

    def move(self):
        self.x += random.randint(-1, 1)
        self.y += random.randint(-1, 1)

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
        if random.random() < self.death_rate:
            self.environment.agents.remove(self)

class Environment:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.agents = [Agent(random.randint(0, width), random.randint(0, height), self) for _ in range(10)] # 10 agents to start
        self.agent_counts = [len(self.agents)]

    def step(self):
        for agent in self.agents:
            agent.move()
            agent.calculate_fitness()
            agent.die()

        # Select agents for reproduction based on fitness
        total_fitness = sum(agent.fitness for agent in self.agents)
        probabilities = [agent.fitness / total_fitness for agent in self.agents]
        new_agents = []
        for i in range(len(self.agents)):
            parent1 = random.choices(self.agents, probabilities)[0]
            parent2 = random.choices(self.agents, probabilities)[0]
            child_x = (parent1.x + parent2.x) / 2
            child_y = (parent1.y + parent2.y) / 2
            new_agents.append(Agent(child_x, child_y, self))

        # Replace old agents with new ones
        self.agents = new_agents

        # Add current number of agents to list
        self.agent_counts.append(len(self.agents))

env = Environment(100, 100)
for i in range(100):
    env.step()
    print(env.agent_counts)