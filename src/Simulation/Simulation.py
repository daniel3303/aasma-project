from __future__ import annotations

from src.Entity.Entity import Entity
from src.World import World


class Simulation:
    entities: list[Entity]
    world: World

    def __init__(self, world: World) -> None:
        self.entities = []
        self.world = world
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
        if(entity.getX() + entity.getWidth() > self.getWorldWidth()):
            entity.setX(self.getWorldWidth()-entity.getWidth())
        if(entity.getY() < 0):
            entity.setY(0)
        if(entity.getY() + entity.getHeight() > self.getWorldHeight()):
            entity.setY(self.getWorldHeight()-entity.getHeight())

    def draw(self, screen) -> Simulation:
        self.world.draw(screen)
        for entity in self.entities:
            entity.draw(screen)

        return self

    def getWorldHeight(self):
        return self.world.getWorldHeight()

    def getWorldWidth(self):
        return self.world.getWorldWidth()


