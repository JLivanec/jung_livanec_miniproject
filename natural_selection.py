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
        self.environment = environment
        self.satiated = False
        self.energy = 15 # starting energy when agent is spawned
        self.speed = 1
        self.movement_cost = self.speed # 1/speed to get step cost, * speed^2 as biological limitation, add'l energy for add'l speed
        self.food_reward = 10 # reward collected for consuming food
        self.stationary_penalty = 1 # penalty for remaining stationary

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

        # determine whether the food is worth consuming
        if dist < (self.energy * self.speed):
            self.shortest_path_step(closest)
            self.eat()   
        else:
            self.energy -= self.stationary_penalty
            self.satiated = True

    def eat(self):
        if ((self.x, self.y) in self.environment.food_grid):
            self.environment.food_grid.remove((self.x, self.y))
            self.energy += self.food_reward

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
        self.avg_energy = []
        self.avg_speed = []

    def populate_food(self):
        self.food_grid = [(random.randint(0, self.width), random.randint(0, self.height)) for _ in range(self.num_food)]

    def kill_the_weak(self):
        self.agents = [agent for agent in self.agents if agent.energy > 0.0]

    def calculate_energy_avg(self):
        energy = [agent.energy for agent in self.agents]
        avg = sum(energy) / len(energy)
        return avg
    
    def calculate_speed_avg(self):
        speed = [agent.speed for agent in self.agents]
        avg = sum(speed) / len(speed)
        return avg

    # function that simulates one generation
    def step(self):
        self.populate_food()
        all_agents_satiated = False

        # move all agents one step at a time until all are satiated
        while not all_agents_satiated:
            satiation = []
            for agent in self.agents:
                agent.move_to_food()
                satiation.append(agent.satiated)
            all_agents_satiated = all(satiation)
        
        # remove agents with energy < 0
        self.kill_the_weak()

        # write metrics to lists for examiniation
        self.remaining_food.append(len(self.food_grid))
        if len(self.agents) > 0:
            self.avg_energy.append(self.calculate_energy_avg())
            self.avg_speed.append(self.calculate_speed_avg())
        else:
            self.avg_energy.append(0)
            self.avg_speed.append(0)

        # REALLOCATION OF SURVIVING AGENTS AND REPRODUCTION
        num_survivors = len(self.agents)
        new_agents = []
        # random mutation occurs with the following odds
        speed_boost = {0 : 10, 1 : 2, 2 : 1}

        for _ in range(num_survivors):
            # all surviving agents persist the next generation
            parent = random.choice(self.agents)
            parent.x = random.randint(0, self.width)
            parent.y = random.randint(0, self.height)
            parent_speed = parent.speed
            new_parent = Agent(parent.x, parent.y, self)
            # all surviving agents will replicate
            new_parent.speed = parent_speed
            new_agents.append(new_parent)
            # speed of child randomly mutates
            speed = parent_speed + random.choices(list(speed_boost.keys()), weights=list(speed_boost.values()), k=1)[0]
            child_agent = Agent(random.randint(0, self.width), random.randint(0, self.height), self)
            child_agent.speed = speed
            new_agents.append(child_agent)
    
        self.agents = new_agents

        # Add current number of agents to list
        self.agent_counts.append(len(self.agents))
        
        return self.agents, self.food_grid

    # Function that generates animation in gif format
    def animate(self, env, iterations):
            
        plt.switch_backend('Agg') # don't show plot
        fig, (ax1, ax2) = plt.subplots(2, 1)
        ax1.set_xlim(0, self.width)
        ax1.set_ylim(0, self.height)
        ax1.set_title('Agents location')
        ax1.set_xlabel('X')
        ax1.set_ylabel('Y')
        
        ax2.set_title('Number of Agents')
        ax2.set_xlabel('Generations')
        ax2.set_ylabel('Number of Agents')
        ax2.set_xlim(0, iterations)
        ax2.set_ylim(0, 30)
        ax2.set_xticks(np.arange(0, iterations, 1))
        
        fig.set_figheight(8)
        fig.set_figwidth(5)
        fig.tight_layout()
        
        scat_agents = ax1.scatter([], [], c='k', s=30, marker='*', label='Agent')
        scat_food = ax1.scatter([], [], c='r', s=30, marker='x', label='Food')
        line_agents, = ax2.plot([], [], c='k') # initialise empty line_agents

        num_agents_list = []

        def update(frame_number):
            agent, food = env.step()
            
            scat_agents.set_offsets(np.c_[[a.x for a in agent], [a.y for a in agent]])
            scat_food.set_offsets(np.c_[[f[0] for f in food], [f[1] for f in food]])
            
            num_agents = len(self.agents)
            ax1.set_title('Agents location - Generation #%i (No. of Agents: %s)' %(frame_number, num_agents))
            
            num_agents_list.append(num_agents)
            line_agents.set_data(range(len(num_agents_list)), num_agents_list)
            
            return scat_agents, line_agents
        
        # Legend for each figure
        ax1.legend(loc='lower center', bbox_to_anchor = (0.5, -0.3), ncol=2)
        plt.subplots_adjust(wspace=0, hspace=0.4)
        
        # interval = delay between frames in milliseconds
        # blit = optimise drawing
        ani = animation.FuncAnimation(fig=fig,
                                        func=update,
                                        frames=iterations,
                                        interval=500,
                                        blit=False,
                                        repeat=True,
                                        )
        mypath = os.path.dirname(os.path.abspath(__file__)) + '/'
        # writergif = animation.PillowWriter(fps=30)
        # ani.save(mypath + "animation.gif", writer=writergif)
        ani.save(mypath + 'animation.gif', writer='pillow')

# DRIVER ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def simulate(iterations, num_agents=10, num_food=100) :
    env = Environment(50, 50, num_agents, num_food)
    env.animate(env, iterations)
    for i in range(iterations) :
        print("Iteration Number " + str(i+1))
        print("Total Population: " + str(env.agent_counts[i]))
        env.step()
        
        if i == iterations - 1 :
            print(env.agent_counts)
            return(env.agent_counts, env.avg_energy, env.avg_speed)