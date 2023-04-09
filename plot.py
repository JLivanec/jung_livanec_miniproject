import matplotlib.pyplot as plt
from natural_selection import simulate
import os

agent_count, food = simulate(10, 100, 1000)

fig, axs = plt.subplots(2)
fig.suptitle("Agent Population and Fitness Over Time")
axs[0].plot(agent_count)
axs[0].set(ylabel="Number of Agents", xlabel="Generations")
axs[1].plot(food)
axs[1].set(ylabel="Remaining Food", xlabel="Generations")

mypath = os.path.dirname(os.path.abspath(__file__)) + '/'
fig.savefig(mypath + "iteration_plot.png")
# plt.show()