import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import os

# AGENT CLASS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Agent:
    def __init__(self, x, y, environment):
        self.x = x
        self.y = y
        self.fitness = 0
        self.environment = environment
        self.death_rate = 0.01
        self.satiated = False
        self.energy = 15
        self.speed = 2
        self.movement_cost = 1 / self.speed
        self.food_reward = 15
        self.stationary_penalty = 0.75

    def manhattan(self, food):
        return (abs(self.x - food[0]) + abs(self.y - food[1]))

    # Movement is completely random
    def move_randomly(self):
        self.x += random.randint(-1, 1)
        self.y += random.randint(-1, 1)

    # take a step length towards closest food
    # this world has no walls, so pathfinding would be unnecessarily expensive
    # we can just move the exact manhattan distance
    def shortest_path_step(self, pos):
        spaces_to_move = self.speed
        pos_x, pos_y = pos
        agent_x = self.x
        agent_y = self.y
        y_delta = pos_y - agent_y
        x_delta = pos_x - agent_x
        consumed = y_delta == 0 and x_delta == 0

        while spaces_to_move > 0 and not consumed:
            if abs(y_delta) > abs(x_delta):
                # move down
                if y_delta < 0:
                    self.y = agent_y - 1
                # move up
                else:
                    self.y = agent_y + 1
            else:
                # move left
                if x_delta < 0:
                    self.x = agent_x - 1
                # move right
                else:
                    self.x = agent_x + 1
            # decrement number of moves in sequence
            spaces_to_move -= 1
            # consume energy for movement
            self.energy -= self.movement_cost
            # reset vars
            agent_x = self.x
            agent_y = self.y
            y_delta = pos_y - agent_y
            x_delta = pos_x - agent_x
            consumed = y_delta == 0 and x_delta == 0
    
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
        #print("distance to food is: " + str(dist) + ", energy is " + str(self.energy))

        # determine whether the food is worth consuming
        if dist < (self.energy * self.speed):
            #print("agent will pursue food located at " + str(closest))
            self.shortest_path_step(closest)
            self.eat()   
        else:
            self.energy -= self.stationary_penalty
            self.satiated = True
            #print("agent remains stationary")

    def eat(self):
        if ((self.x, self.y) in self.environment.food_grid):
            self.environment.food_grid.remove((self.x, self.y))
            self.energy += self.food_reward
            #print("agent has eaten")

    def die(self):
        self.environment.agents.remove(self)

# ENVIRONMENT CLASS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Environment:
    def __init__(self, width, height, num_agents, num_food):
        self.width = width
        self.height = height
        self.num_food = num_food
        self.agents = [Agent(random.randint(0, width), random.randint(0, height), self) for _ in range(num_agents)] # 10 agents to start
        self.agent_counts = [len(self.agents)]
        self.food_grid = []
        self.remaining_food = []
        self.avg_energy = 0

    def populate_food(self):
        self.food_grid = [(random.randint(0, self.width), random.randint(0, self.height)) for _ in range(self.num_food)]

    def kill_the_weak(self):
        self.agents = [agent for agent in self.agents if agent.energy > 0.0]

    def step(self):
        self.populate_food()
        all_agents_satiated = False
        while not all_agents_satiated:
            #print("ROUND OF MOVEMENT, NOT ALL AGENTS SATIATED")
            satiation = []
            for agent in self.agents:
                #print("agent position: (" + str(agent.x) + ", " + str(agent.y) + ")")
                agent.move_to_food()
                #print("agent position after step: (" + str(agent.x) + ", " + str(agent.y) + ")")
                #if agent.satiated:
                #    print("agent is satiated")
                #else:
                #    print("agent still hungry")
                satiation.append(agent.satiated)
            all_agents_satiated = all(satiation)
        
        self.kill_the_weak()

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

    def animate(self):
        plt.switch_backend('Agg') # don't show plot
        fig, ax = plt.subplots()
        ax.set_xlim(0,self.width)
        ax.set_ylim(0,self.height)
        scat_agents = ax.scatter([a.x for a in self.agents], [a.y for a in self.agents], c='k', s=3, marker='*')
        scat_food = ax.scatter([f[0] for f in self.food_grid], [f[1] for f in self.food_grid], c='r', s=3, marker='x')
        ax.set_title('Agents location')

        def update(frame_number):
            for agent in self.agents:
                agent.move_to_food()
                agent.eat()
                # agent.calculate_fitness()
                if random.random() < agent.death_rate:
                    agent.die()
            scat_agents.set_offsets(np.c_[[a.x for a in self.agents], [a.y for a in self.agents]])
            scat_food.set_offsets(np.c_[[f[0] for f in self.food_grid], [f[1] for f in self.food_grid]])
            return scat_agents,

        ani = animation.FuncAnimation(fig=fig,
                                        func=update,
                                        frames=100,
                                        interval=5,
                                        blit=True)
        mypath = os.path.dirname(os.path.abspath(__file__)) + '/'
        # writergif = animation.PillowWriter(fps=30)
        # ani.save(mypath + "animation.gif", writer=writergif)
        ani.save(mypath + 'animation.gif', writer='pillow')

# DRIVER ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def simulate(iterations, num_agents=10, num_food=100) :
    env = Environment(50, 50, num_agents, num_food)
    #env.animate() # create animation
    for i in range(iterations) :
        print("Iteration Number " + str(i+1))
        print("Remaining Survivors: " + str(env.agent_counts[i]))
        env.step()
        
        if i == iterations - 1 :
            print(env.agent_counts)
            return(env.agent_counts, env.remaining_food)