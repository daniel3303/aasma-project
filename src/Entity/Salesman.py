import pygame

from src.Entity.Entity import Entity


class Salesman(Entity):

    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        super().__init__(x, y, width, height)

    def draw(self, screen) -> Entity:
        pygame.draw.rect(screen, (255, 0, 0), (self.getX(), self.getX(), self.getWidth(), self.getHeight()))
        return self
