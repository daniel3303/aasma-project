import sys

import pygame
from src.Entity.Salesman import Salesman
from src.Simulation.Simulation import Simulation
from src.Walk.RandomWalker import RandomWalker
from src.World import World

pygame.init()

pygame.display.set_caption("AASMA Project")

world = World()
simulation = Simulation(world)
screen = pygame.display.set_mode((world.getWorldWidth(),world.getWorldHeight()))

salesman = Salesman(300,300,50,50, 6)
salesman.setWalker(RandomWalker())
simulation.addEntity(salesman)



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    simulation.update()
    screen.fill((255,255,255))
    simulation.draw(screen)
    pygame.display.update()
