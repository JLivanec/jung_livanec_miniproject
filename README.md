# Hacking Natural Selection
## Jinsol Jung, Jackson Livanec
## CS 5804
---
## Description
This project simulates natural selection and random mutation as an aspect of evolution. The randomly mutating speed trait is recorded over a number of generations as agents race to consume enough food to out-survive the others.

## Game Description and Rules
Beginning at generation 0, agents and food are randomly spawned into a rectangular environment. Key agent field variables are `energy` and `speed`. Agents are started with a finite amount of energy and a speed of 1. Each timestep, all agents will search for the closest piece of food and determine whether the energy expenditure associated with moving to that food will be net positive. If the agent chooses to move to that food, it will expend energy at the rate speed $^{2}$. Simultaneous decision making often leads to competition over a single piece of food. Food consumption results in an energy reward to the consuming agent. The consumed food will no longer be available for other agents.

If an agent determines that the closest food is not worth the energy expenditure, it will remain stationary and constantly lose energy at a rate less than movement alone. It flags itself as "satiated" via the field variable `Agent.satiated==True`. A generation is complete when all agents are satiated.

The conclusion of a generation removes all agents depleted of energy. All surviving agents spawn successors with matching traits. There is a small probability that the speed trait will mutate and increase. All new and surviving agents are then randomly distributed into the environment with a new distribution of food. The amount of food available to the entire population remains constant to simulate scarcity and competition.

## Variables and Parameters
There are a number of parameters that determine agent behavior that can be manipulated for insightful reporting.

* `simulate(iterations, num_agents, num_food)` is the main driver function and captures three arguments, `iterations`: the number of generations to run in the simulation, `num_agents`: the number of agents to randomly distribute in the environment for generation 1, and `num_food`: the amount of food to randomly distribute in the environment each generation.
* `Environment()` class is passed the former variables, with the addition of `height` and `width` describing the shape of the environment.
* `Agent.energy` can be tuned and represents the amount of energy the newly spawned agent has before any food consumption. This value is necessary for the agent to make the journey to its first piece of food.
* `Agent.food_reward` can be tuned and represents the amount of energy rewarded to the agent when food is consumed.
* `Agent.stationary_penalty` can be tuned and represents the penalty on energy each timestep that the agent remains stationary. This penalty discourages agents from retaining their initial energy assignment instead of searching for food when there is scarcity.
* `speed_boost` is a dictionary representing possible mutations to the `speed` value and their associated probabilities. The default values are `{0:10, 1:2, 2:1}`
