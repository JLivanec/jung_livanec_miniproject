import matplotlib.pyplot as plt
import matplotlib.animation as animation
from natural_selection import simulate
import os

# input for simulation:
# 1. number of total generations to run
# 2. number of agents at start of simulation
# 3. number of food items for agents to consume at each generation
population, food, speed, size = simulate(20, 10, 50)

fig, axs = plt.subplots(3)
fig.suptitle("Agent Population Speed, and Size Over Time")
axs[0].plot(population)
axs[0].set(ylabel="Population of Agents", xlabel="Generations")
axs[1].plot(speed)
axs[1].set(ylabel="Average Agent Speed", xlabel="Generations")
axs[2].plot(size)
axs[2].set(ylabel="Average Agent Size", xlabel="Generations")

#mypath = os.path.dirname(os.path.abspath(__file__)) + '/'
#fig.savefig(mypath + "iteration_plot.png")
plt.show()