import sys

import pygame

from src.Entity.Consumer import Consumer
from src.Entity.Salesman import Salesman
from src.Math.Vector2D import Vector2D
from src.Simulation.Simulation import Simulation
from src.World import World

pygame.init()

pygame.display.set_caption("AASMA Project")

world = World()
simulation = Simulation(world)
screen = pygame.display.set_mode((world.getWorldWidth(),world.getWorldHeight()))

for i in range(0,9):
    consumer = Consumer(simulation, Vector2D(190, 30), Vector2D(25,25))
    simulation.addEntity(consumer)

for i in range(0,1):
    salesman = Salesman(simulation, Vector2D(200,100), Vector2D(25,25))
    simulation.addEntity(salesman)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    simulation.update()
    screen.fill((255,255,255))
    simulation.draw(screen)
    pygame.display.update()
    pygame.time.wait(1000//60)

