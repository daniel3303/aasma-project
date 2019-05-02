from __future__ import annotations

from src.Entity.Entity import Entity


class Simulation:
    entities: list[Entity]
    worldWidth: int
    worldHeight: int

    def __init__(self, worldWidth: int, worldHeight:int) -> None:
        self.entities = []
        self.worldWidth = worldWidth
        self.worldHeight = worldHeight
        pass

    def addEntity(self, entity: Entity) -> Simulation:
        self.entities.append(entity)
        return self

    def update(self) -> None:
        for entity in self.entities :
            entity.update()
            self.forceInBound(entity)

    def forceInBound(self, entity: Entity):
        if(entity.getX() < 0):
            entity.setX(0)
        if(entity.getX() + entity.getWidth() > self.worldWidth):
            entity.setX(self.worldWidth-entity.getWidth())
        if(entity.getY() < 0):
            entity.setY(0)
        if(entity.getY() + entity.getHeight() > self.worldHeight):
            entity.setY(self.worldHeight-entity.getHeight())

    def draw(self, screen) -> Simulation:
        for entity in self.entities:
            entity.draw(screen)

        return self

    def getWorldHeight(self):
        return self.worldHeight

    def getWorldWidth(self):
        return self.worldWidth


