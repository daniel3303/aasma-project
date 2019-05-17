import csv
import os
import tensorflow as tf

from src.Agent.DeepLearningAgent.DeepLearningAgent import DeepLearningAgent
from src.Agent.Reactive.ReactiveAgent import ReactiveAgent
from src.Entity.Consumer import Consumer
from src.Entity.HotSpot import HotSpot
from src.Entity.Salesman import Salesman
from src.Math.Vector2D import Vector2D
from src.Simulation.Simulation import Simulation
from src.World import World


salesmanA = None
salesmanB = None
simulation = None

def create_simulation_reactive_vs_deep_q():
    global salesmanA, salesmanB, simulation

    tf.reset_default_graph()

    world = World()
    simulation = Simulation(world)

    hotspot = HotSpot(simulation, Vector2D(50, 50), Vector2D(50, 50))
    simulation.addEntity(hotspot)

    hotspot = HotSpot(simulation, Vector2D(200, 650), Vector2D(50, 50))
    simulation.addEntity(hotspot)

    # Consumers
    for i in range(0, 4):
        consumer = Consumer(simulation, simulation.getRandomEmptyPlace(), Vector2D(50, 50))
        simulation.addEntity(consumer)

    # Reactive agent
    salesmanA = Salesman(simulation, simulation.getRandomEmptyPlace(), Vector2D(50, 50))
    agent = ReactiveAgent(salesmanA)
    simulation.addEntity(salesmanA)
    simulation.addAgent(agent)

    # Deep Q Learning Agent
    salesmanB = Salesman(simulation, simulation.getRandomEmptyPlace(), Vector2D(50, 50))
    agent = DeepLearningAgent(salesmanB, model="reactive_vs_deep_learning/episode_136")
    simulation.addEntity(salesmanB)
    simulation.addAgent(agent)

def create_simulation_reactive_vs_reactive():
    global salesmanA, salesmanB, simulation

    tf.reset_default_graph()

    world = World()
    simulation = Simulation(world)

    hotspot = HotSpot(simulation, Vector2D(50, 50), Vector2D(50, 50))
    simulation.addEntity(hotspot)

    hotspot = HotSpot(simulation, Vector2D(200, 650), Vector2D(50, 50))
    simulation.addEntity(hotspot)

    # Consumers
    for i in range(0, 4):
        consumer = Consumer(simulation, simulation.getRandomEmptyPlace(), Vector2D(50, 50))
        simulation.addEntity(consumer)

    # Reactive agent
    salesmanA = Salesman(simulation, simulation.getRandomEmptyPlace(), Vector2D(50, 50))
    agent = ReactiveAgent(salesmanA)
    simulation.addEntity(salesmanA)
    simulation.addAgent(agent)

    # Deep Q Learning Agent
    salesmanB = Salesman(simulation, simulation.getRandomEmptyPlace(), Vector2D(50, 50))
    agent = ReactiveAgent(salesmanB)
    simulation.addEntity(salesmanB)
    simulation.addAgent(agent)

def create_simulation_deep_q_vs_deep_q(iterationA="", iterationB=""):
    global salesmanA, salesmanB, simulation

    tf.reset_default_graph()

    world = World()
    simulation = Simulation(world)

    hotspot = HotSpot(simulation, Vector2D(50, 50), Vector2D(50, 50))
    simulation.addEntity(hotspot)

    hotspot = HotSpot(simulation, Vector2D(200, 650), Vector2D(50, 50))
    simulation.addEntity(hotspot)

    # Consumers
    for i in range(0, 4):
        consumer = Consumer(simulation, simulation.getRandomEmptyPlace(), Vector2D(50, 50))
        simulation.addEntity(consumer)

    # Deep Q Learning Agent
    salesmanA = Salesman(simulation, simulation.getRandomEmptyPlace(), Vector2D(50, 50))
    agent = DeepLearningAgent(salesmanA, model="reactive_vs_deep_learning/episode_"+iterationA)
    simulation.addEntity(salesmanA)
    simulation.addAgent(agent)

    # Deep Q Learning Agent
    salesmanB = Salesman(simulation, simulation.getRandomEmptyPlace(), Vector2D(50, 50))
    agent = DeepLearningAgent(salesmanB, model="reactive_vs_deep_learning/episode_"+iterationB)
    simulation.addEntity(salesmanB)
    simulation.addAgent(agent)



NUM_EPISODES = 10
MAX_EPISODE_SIZE = 2000

# Reactive vs Deep Q Learning
for episode in range(0, NUM_EPISODES):
    create_simulation_reactive_vs_deep_q()

    if not os.path.exists("data/reactive_vs_deep"):
        os.makedirs("data/reactive_vs_deep")

    with open("data/reactive_vs_deep/run_"+str(episode)+".csv", 'w+') as file:
        wr = csv.writer(file, quoting=csv.QUOTE_ALL)
        wr.writerow(["Reactive Agent", "Deep Learning Agent"])

        for index in range(0, MAX_EPISODE_SIZE):
            simulation.update()
            simulation.outputToConsole()
            wr.writerow([salesmanA.getTotalReward(), salesmanB.getTotalReward()])


# Reactive vs Reactive
for episode in range(0, NUM_EPISODES):
    create_simulation_reactive_vs_reactive()

    if not os.path.exists("data/reactive_vs_reactive"):
        os.makedirs("data/reactive_vs_reactive")

    with open("data/reactive_vs_reactive/run_"+str(episode)+".csv", 'w+') as file:
        wr = csv.writer(file, quoting=csv.QUOTE_ALL)
        wr.writerow(["Reactive Agent", "Reactive Agent"])

        for index in range(0, MAX_EPISODE_SIZE):
            simulation.update()
            simulation.outputToConsole()
            wr.writerow([salesmanA.getTotalReward(), salesmanB.getTotalReward()])


# Deep Q Learning (136) vs Deep Q Learning (136)
for episode in range(0, NUM_EPISODES):
    create_simulation_deep_q_vs_deep_q("136", "136")

    if not os.path.exists("data/deep_136_vs_deep_136"):
        os.makedirs("data/deep_136_vs_deep_136")

    with open("data/deep_136_vs_deep_136/run_"+str(episode)+".csv", 'w+') as file:
        wr = csv.writer(file, quoting=csv.QUOTE_ALL)
        wr.writerow(["Deep Learning Agent (136)", "Deep Learning Agent (136)"])

        for index in range(0, MAX_EPISODE_SIZE):
            simulation.update()
            simulation.outputToConsole()
            wr.writerow([salesmanA.getTotalReward(), salesmanB.getTotalReward()])


# Deep Q Learning (50) vs Deep Q Learning (136)
for episode in range(0, NUM_EPISODES):
    create_simulation_deep_q_vs_deep_q("50", "136")

    if not os.path.exists("data/deep_50_vs_deep_136"):
        os.makedirs("data/deep_50_vs_deep_136")

    with open("data/deep_50_vs_deep_136/run_"+str(episode)+".csv", 'w+') as file:
        wr = csv.writer(file, quoting=csv.QUOTE_ALL)
        wr.writerow(["Deep Learning Agent (50)", "Deep Learning Agent (136)"])

        for index in range(0, MAX_EPISODE_SIZE):
            simulation.update()
            simulation.outputToConsole()
            wr.writerow([salesmanA.getTotalReward(), salesmanB.getTotalReward()])


# Deep Q Learning (0) vs Deep Q Learning (136)
for episode in range(0, NUM_EPISODES):
    create_simulation_deep_q_vs_deep_q("0", "136")

    if not os.path.exists("data/deep_0_vs_deep_136"):
        os.makedirs("data/deep_0_vs_deep_136")

    with open("data/deep_0_vs_deep_136/run_"+str(episode)+".csv", 'w+') as file:
        wr = csv.writer(file, quoting=csv.QUOTE_ALL)
        wr.writerow(["Deep Learning Agent (0)", "Deep Learning Agent (136)"])

        for index in range(0, MAX_EPISODE_SIZE):
            simulation.update()
            simulation.outputToConsole()
            wr.writerow([salesmanA.getTotalReward(), salesmanB.getTotalReward()])


