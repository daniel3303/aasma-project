import sys

import pygame
from src.Entity.Salesman import Salesman
from src.Simulation.Simulation import Simulation
from src.Walk.RandomWalker import RandomWalker

pygame.init()
screen = pygame.display.set_mode((600,600))

pygame.display.set_caption("AASMA Project")

simulation = Simulation(600,600)

salesman = Salesman(300,300,50,50, 6)
salesman.setWalker(RandomWalker())
simulation.addEntity(salesman)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    simulation.update()
    screen.fill((0,0,0))
    simulation.draw(screen)
    pygame.display.update()
