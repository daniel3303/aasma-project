from src.Agent.DeepLearningAgent.DeepLearningAgent import DeepLearningAgent
from src.Agent.Reactive.ReactiveAgent import ReactiveAgent
from src.Entity.Consumer import Consumer
from src.Entity.HotSpot import HotSpot
from src.Entity.Salesman import Salesman
from src.Math.Vector2D import Vector2D
from src.Simulation.Simulation import Simulation
from src.World import World

MAX_EPISODE_SIZE = 500


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


# Reactive agent
salesman = Salesman(simulation, Vector2D(200,100), Vector2D(25,25))
agent = ReactiveAgent(salesman)
simulation.addEntity(salesman)
simulation.addAgent(agent)

# Deep Q Learning Agent
salesman = Salesman(simulation, Vector2D(200,100), Vector2D(25,25))
agent = DeepLearningAgent(salesman)
simulation.addEntity(salesman)
simulation.addAgent(agent)


for i in range(0, MAX_EPISODE_SIZE):
    simulation.update()
    simulation.outputToConsole()

