import sys

import pygame
from src.Entity.Entity import Entity
from src.Entity.Salesman import Salesman
from src.Simulation.Simulation import Simulation

pygame.init()
screen = pygame.display.set_mode((500,500))

pygame.display.set_caption("AASMA Project")

simulation = Simulation()
simulation.addEntity(Salesman(0,0,50,50))
simulation.addEntity(Salesman(300,300,50,50))



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    pygame.time.delay(30)

    simulation.draw(screen)
    pygame.display.update()