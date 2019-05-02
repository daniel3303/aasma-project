import pygame

from src.Entity.Entity import Entity


class Salesman(Entity):

    def __init__(self, x: int, y: int, width: int, height: int, velocity: int) -> None:
        super().__init__(x, y, width, height, velocity)

