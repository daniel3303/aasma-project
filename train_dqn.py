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

MAX_EPISODE_SIZE = 6000

def create_simulation_with_consumers() -> Simulation:
    world = World()
    simulation = Simulation(world)

    hotspot = HotSpot(simulation, Vector2D(150, 150), Vector2D(50, 50))
    simulation.addEntity(hotspot)

    hotspot = HotSpot(simulation, Vector2D(200, 650), Vector2D(50, 50))
    simulation.addEntity(hotspot)

    # Consumers
    for i in range(0, 4):
        consumer = Consumer(simulation, simulation.getRandomEmptyPlace(), Vector2D(50, 50))
        simulation.addEntity(consumer)
    return simulation




def play_one(model, tmodel, eps, gamma, copy_period):
    simulation = create_simulation_with_consumers()

    # Reactive agent
    #salesman = Salesman(simulation, Vector2D(50, 50), Vector2D(50, 50))
    #agent = ReactiveAgent(salesman)
    #simulation.addEntity(salesman)
    #simulation.addAgent(agent)

    # Deep Q Learning Agent
    salesman = Salesman(simulation, simulation.getRandomEmptyPlace(), Vector2D(50, 50))
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
        model.add_experience(prev_observation, action, reward, observation)
        model.train(tmodel)


        #print("EXPERINCES")
        #model.printExperience()

        iters += 1
        print(" iter: " + str(iters) + "/" + str(MAX_EPISODE_SIZE) + " ", end="")

        if iters % copy_period == 0:
            tmodel.copy_from(model)
            #print("\n\nFroze new version of the model")
            #print("Current Q (tmodel) at (50,50): ")
            #model.print_Q([[50, 50] + [0]*12, [50, 50] + [0,0,1] * 4], tmodel)
            #print("Current Q (tmodel) at (50,350): ")
            #model.print_Q([[50, 350] + [0]*12, [50, 350] + [0,0,1] * 4], tmodel)
            #print("")

    #print("Current Q (tmodel): ")
    #print(model.print_Q([[0, 0], [15, 0], [0, 15], [15, 15]], tmodel))
    #print("EXPERINCES")
    #model.printExperience()


    return totalreward


def main():
    gamma = 0.9
    copy_period = 3000

    D = 14 #fix me make it dynamic
    K = 5 #fix me make it dynamic

    sizes = [16384]
    model = DQN(D, K, sizes, gamma)
    tmodel = DQN(D, K, sizes, gamma)
    session = tf.InteractiveSession()
    init = tf.global_variables_initializer()
    session.run(init)

    model.set_session(session)
    tmodel.set_session(session)

    saver = tf.train.Saver(max_to_keep=0)

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
            save_path = saver.save(session, "models/episode_"+str(n)+".ckpt")
            print("Episode's model saved at "+save_path)

    save_path = saver.save(session, "models/final_model.ckpt")
    print("Final model saved at "+save_path)

    print("avg reward for last 100 episodes:", totalrewards[-100:].mean())
    print("total steps:", totalrewards.sum())


if __name__ == '__main__':
    main()

