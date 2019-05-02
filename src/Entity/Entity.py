from __future__ import annotations

class Entity:
    x: int
    y: int

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def getX(self) -> int:
        return self.x

    def getY(self) -> int:
        return self.y

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


