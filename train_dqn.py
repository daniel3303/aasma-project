import tensorflow as tf
import numpy as np
import sys
import os

from src.Agent.DeepLearningAgent.DeepLearningAgent import DeepLearningAgent, DQN, save_model, load_modal
from src.Agent.Reactive.ReactiveAgent import ReactiveAgent
from src.Entity.Consumer import Consumer
from src.Entity.HotSpot import HotSpot
from src.Entity.Salesman import Salesman
from src.Math.Vector2D import Vector2D
from src.Simulation.Simulation import Simulation
from src.World import World

MAX_EPISODE_SIZE = 2000

def create_simulation_with_consumers() -> Simulation:
    world = World()
    simulation = Simulation(world)

    hotspot = HotSpot(simulation, Vector2D(30,30), Vector2D(25,25))
    simulation.addEntity(hotspot)

    hotspot = HotSpot(simulation, Vector2D(300,75), Vector2D(25,25))
    simulation.addEntity(hotspot)

    hotspot = HotSpot(simulation, Vector2D(75,300), Vector2D(25,25))
    simulation.addEntity(hotspot)

    hotspot = HotSpot(simulation, Vector2D(300,300), Vector2D(25,25))
    simulation.addEntity(hotspot)


    for i in range(0,8):
        consumer = Consumer(simulation, Vector2D(190, 30), Vector2D(25,25))
        simulation.addEntity(consumer)

    return simulation




def play_one(model, eps, gamma):
    simulation = create_simulation_with_consumers()

    # Reactive agent
    salesman = Salesman(simulation, Vector2D(50, 50), Vector2D(25, 25))
    agent = ReactiveAgent(salesman)
    simulation.addEntity(salesman)
    simulation.addAgent(agent)

    # Deep Q Learning Agent
    salesman = Salesman(simulation, Vector2D(50, 50), Vector2D(25, 25))
    agent = DeepLearningAgent(salesman)
    simulation.addEntity(salesman)
    simulation.addAgent(agent)

    observation = agent.getCurrentObservation()
    totalreward = 0
    iters = 0

    while iters < MAX_EPISODE_SIZE:
        action = model.sample_action(observation, eps)
        prev_observation = observation

        agent.setNextAction(action)

        # update the simulation
        simulation.update()
        simulation.outputToConsole()

        # extract iteration data
        observation = agent.getCurrentObservation()
        reward = agent.getCurrentReward()

        totalreward += reward

        # update the model
        done = False
        if iters == MAX_EPISODE_SIZE - 1:
            done = True
        model.add_experience(prev_observation, action, reward, observation, done)
        model.train()

        print(" iter: "+str(iters)+"/"+str(MAX_EPISODE_SIZE)+" ", end="")

        iters += 1

    return totalreward


def main():
    gamma = 0.99
    D = 26 #fix me make it dynamic
    K = 5 #fix me make it dynamic

    sizes = [64, 64]
    model = DQN(D, K, sizes, gamma)
    session = tf.InteractiveSession()
    init = tf.global_variables_initializer()
    session.run(init)

    model.set_session(session)

    N = 2000
    totalrewards = np.empty(N)
    for n in range(N):
        eps = 1 / np.sqrt(n + 1)
        totalreward = play_one(model, eps, gamma)
        totalrewards[n] = totalreward

        print("episode:", n, "total reward:", totalreward, "eps:", eps, "avg reward (last 100):",
                  totalrewards[max(0, n - 100):(n + 1)].mean())

if __name__ == '__main__':
    main()

