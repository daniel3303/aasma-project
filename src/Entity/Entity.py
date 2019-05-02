from __future__ import annotations

from src.Exception.MethodNotImplementedException import MethodNotImplementedException


class Entity:
    x: int
    y: int
    width: int
    height: int

    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def getX(self) -> int:
        return self.x

    def getY(self) -> int:
        return self.y

    def getWidth(self) -> int:
        return self.width

    def getHeight(self) -> int:
        return self.height

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

    def update(self, deltaTime: float) -> Entity:
        return self

    def draw(self, screen) -> Entity:
        raise MethodNotImplementedException()


