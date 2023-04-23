import matplotlib.pyplot as plt
import matplotlib.animation as animation
from natural_selection import simulate
import os

population, food, speed = simulate(20, 10, 50)

fig, axs = plt.subplots(2)
fig.suptitle("Agent Population and Speed Over Time")
axs[0].plot(population)
axs[0].set(ylabel="Population of Agents", xlabel="Generations")
axs[1].plot(speed)
axs[1].set(ylabel="Average Agent Speed", xlabel="Generations")

mypath = os.path.dirname(os.path.abspath(__file__)) + '/'
fig.savefig(mypath + "iteration_plot.png")
plt.show()