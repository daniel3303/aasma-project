import tensorflow as tf
import numpy as np
import sys
import os
import time

from src.Agent.DeepLearningAgent.DeepLearningAgent import DeepLearningAgent, DQN
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

    hotspot = HotSpot(simulation, Vector2D(25, 25), Vector2D(25, 25))
    simulation.addEntity(hotspot)

    hotspot = HotSpot(simulation, Vector2D(250, 75), Vector2D(25, 25))
    simulation.addEntity(hotspot)

    hotspot = HotSpot(simulation, Vector2D(75, 300), Vector2D(25, 25))
    simulation.addEntity(hotspot)

    hotspot = HotSpot(simulation, Vector2D(200, 200), Vector2D(25, 25))
    simulation.addEntity(hotspot)


    for i in range(0,6):
        consumer = Consumer(simulation, Vector2D(25, 25), Vector2D(25,25))
        simulation.addEntity(consumer)

    return simulation




def play_one(model, tmodel, eps, gamma, copy_period):
    simulation = create_simulation_with_consumers()

    # Reactive agent
    salesman = Salesman(simulation, Vector2D(25, 25), Vector2D(25, 25))
    agent = ReactiveAgent(salesman)
    simulation.addEntity(salesman)
    simulation.addAgent(agent)

    # Deep Q Learning Agent
    salesman = Salesman(simulation, Vector2D(25, 25), Vector2D(25, 25))
    agent = DeepLearningAgent(salesman)
    simulation.addEntity(salesman)
    simulation.addAgent(agent)

    observation = agent.getCurrentObservation()
    totalreward = 0
    iters = 0

    while iters < MAX_EPISODE_SIZE:
        #print("\n\n")
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
        model.train(tmodel)



        """print("\nPrev State: "+str(prev_observation))
        print("Action: "+str(action))
        print("Next State: "+str(observation))
        print("Current Q (tmodel): ")
        print(model.print_Q([[0,0], [15,0], [0,15], [15,15]], tmodel))"""

        #print("EXPERINCES")
        #model.printExperience()

        iters += 1
        print(" iter: " + str(iters) + "/" + str(MAX_EPISODE_SIZE) + " ", end="")

        if iters % copy_period == 0:
            tmodel.copy_from(model)

    #print("Current Q (tmodel): ")
    #print(model.print_Q([[0, 0], [15, 0], [0, 15], [15, 15]], tmodel))
    #print("EXPERINCES")
    #model.printExperience()


    return totalreward


def main():
    gamma = 0.95
    copy_period = 2000

    D = 20 #fix me make it dynamic
    K = 5 #fix me make it dynamic

    sizes = [512, 512]
    model = DQN(D, K, sizes, gamma)
    tmodel = DQN(D, K, sizes, gamma)
    session = tf.InteractiveSession()
    init = tf.global_variables_initializer()
    session.run(init)

    model.set_session(session)
    tmodel.set_session(session)

    saver = tf.train.Saver()

    N = 2000
    totalrewards = np.empty(N)
    for n in range(N):
        eps = 1.0 / np.sqrt(n + 1)
        if n % 5 == 0 and n > 0:
            eps = 0
        totalreward = play_one(model, tmodel, eps, gamma, copy_period)
        totalrewards[n] = totalreward

        if n % 1 == 0:
            print("episode:", n, "total reward:", totalreward, "eps:", eps, "avg reward (last 100):",
                  totalrewards[max(0, n - 100):(n + 1)].mean())

        if n % 50 == 0:
            save_path = saver.save(session, "models/episode_"+str(n)+".ckpt")
            print("Episode's model saved at "+save_path)

    save_path = saver.save(session, "models/final_model.ckpt")
    print("Final model saved at "+save_path)

    print("avg reward for last 100 episodes:", totalrewards[-100:].mean())
    print("total steps:", totalrewards.sum())


if __name__ == '__main__':
    main()

