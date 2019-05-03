from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from src.Walk.Walker import Walker


class Entity:
    x: int
    y: int
    width: int
    height: int
    velocity:int
    walker: Walker
    image: pygame.Surface

    def __init__(self, x: int, y: int, width: int, height: int, velocity: int) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = velocity
        self.walker = None
        self.image = None

    def setImage(self, image):
        self.image = pygame.transform.scale(image, (self.getWidth(), self.getHeight()))

    def getX(self) -> int:
        return self.x

    def getY(self) -> int:
        return self.y

    def getWidth(self) -> int:
        return self.width

    def getHeight(self) -> int:
        return self.height

    def getVelocity(self) -> int:
        return self.velocity

    def getWalker(self) -> Walker:
        return self.walker

    def getTopSensor(self) -> (int, int):
        return (self.getX() + self.getWidth()/2, self.getY())

    def getBottomSensor(self) -> (int, int):
        return (self.getX() + self.getWidth()/2, self.getY() + self.getHeight())

    def getLeftSensor(self) -> (int, int):
        return (self.getX(), self.getY() + self.getHeight()/2)

    def getRightSensor(self) -> (int, int):
        return (self.getX() + self.getWidth(), self.getY() + self.getHeight()/2)

    def setX(self, x: int) -> Entity:
        self.x = x
        return self

    def setY(self, y: int) -> Entity:
        self.y = y
        return self

    def moveX(self, x: int) -> Entity:
        self.x += x
        return self

    def moveY(self, y: int) -> Entity:
        self.y += y
        return self

    def setWalker(self, walker: Walker) -> Entity:
        self.walker = walker
        if(walker.getEntity() != self):
            walker.setEntity(self)
        return self

    def getRect(self):
        return pygame.Rect(self.getX(), self.getY(), self.getWidth(), self.getHeight())

    def update(self) -> Entity:
        if(self.walker):
            self.walker.walk()
        return self

    def draw(self, screen) -> Entity:
        if(self.image != None):
            screen.blit(self.image, (self.getX(), self.getY()))
        else:
            pygame.draw.rect(screen, (255, 0, 0), (self.getX(), self.getY(), self.getWidth(), self.getHeight()))
        return self


