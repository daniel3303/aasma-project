import sys

import pygame

from src.Agent.DeepLearningAgent.DeepLearningAgent import DeepLearningAgent
from src.Agent.Reactive.ReactiveAgent import ReactiveAgent
from src.Entity.Consumer import Consumer
from src.Entity.HotSpot import HotSpot
from src.Entity.Salesman import Salesman
from src.Math.Vector2D import Vector2D
from src.Simulation.Simulation import Simulation
from src.World import World

pygame.init()

pygame.display.set_caption("AASMA Project")

world = World()
simulation = Simulation(world)
screen = pygame.display.set_mode((world.getWorldWidth(),world.getWorldHeight()))

hotspot = HotSpot(simulation, Vector2D(30,30), Vector2D(25,25))
simulation.addEntity(hotspot)

hotspot = HotSpot(simulation, Vector2D(300,75), Vector2D(25,25))
simulation.addEntity(hotspot)

hotspot = HotSpot(simulation, Vector2D(75,300), Vector2D(25,25))
simulation.addEntity(hotspot)

hotspot = HotSpot(simulation, Vector2D(300,300), Vector2D(25,25))
simulation.addEntity(hotspot)


for i in range(0, 8):
    consumer = Consumer(simulation, Vector2D(190, 30), Vector2D(25, 25))
    simulation.addEntity(consumer)

# Reactive agent
salesman = Salesman(simulation, Vector2D(50, 50), Vector2D(25, 25))
agent = ReactiveAgent(salesman)
simulation.addEntity(salesman)
simulation.addAgent(agent)

# Deep Q Learning Agent
salesman = Salesman(simulation, Vector2D(50, 50), Vector2D(25, 25))
agent = DeepLearningAgent(salesman, model="reactive_vs_deep")
#agent = DeepLearningAgent(salesman, model="test")
simulation.addEntity(salesman)
simulation.addAgent(agent)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    simulation.update()
    screen.fill((255,255,255))
    simulation.draw(screen)
    pygame.display.update()
    pygame.time.wait(1000//60)

