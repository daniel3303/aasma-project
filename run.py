import sys

import pygame

from src.Entity.Consumer import Consumer
from src.Entity.Salesman import Salesman
from src.Simulation.Simulation import Simulation
from src.Walk.FollowWalker import FollowWalker
from src.Walk.RandomWalker import RandomWalker
from src.World import World

pygame.init()

pygame.display.set_caption("AASMA Project")

world = World()
simulation = Simulation(world)
screen = pygame.display.set_mode((world.getWorldWidth(),world.getWorldHeight()))


for i in range(0,9):
    consumer = Consumer(190,30,25,25, 18)
    consumer.setWalker(RandomWalker())
    simulation.addEntity(consumer)

for i in range(0,3):
    salesman = Salesman(200, 100, 25, 25, 18)
    salesman.setWalker(RandomWalker())
    simulation.addEntity(salesman)
    simulation.addEntity(salesman)



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    simulation.update()
    screen.fill((255,255,255))
    simulation.draw(screen)
    pygame.display.update()
    pygame.time.wait(1000//60)

