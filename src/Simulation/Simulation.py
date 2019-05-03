from __future__ import annotations

from math import sqrt
from random import randint

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

        # check entities contact
        for entity in self.entities:
            for target in self.entities:
                if(entity != target):
                    if(self.openViewBetween(entity, target) and self.distanceBetween(entity, target) <= entity.getViewRange()):
                        entity.sees(target)
                    else:
                        entity.dontSees(target)


    def openViewBetween(self, a: Entity, b: Entity):
        vec = (b.getX() - a.getX(), b.getY() - a.getY())
        vecLen = sqrt(vec[0] ** 2 + vec[1]**2)
        if(vecLen == 0):
            return True
        totalSteps = int(vecLen)

        normalizedVec = (vec[0]/vecLen, vec[1]/vecLen)

        for step in range(0, totalSteps):
            x = a.getX() + normalizedVec[0] * step
            y = a.getY() + normalizedVec[1] * step

            tile = self.world.getTileAt((x,y))
            if(self.world.isWall(tile)):
                return False

        return True

    def distanceBetween(self, a: Entity, b: Entity):
        return sqrt(((a.getX() - b.getX())**2 + (a.getY() - b.getY())**2))


    def forceInBound(self, entity: Entity):
        if(entity.getX() < 0):
            entity.setX(0)
        if(entity.getX() + entity.getWidth() > self.getWorldWidth()):
            entity.setX(self.getWorldWidth()-entity.getWidth())
        if(entity.getY() < 0):
            entity.setY(0)
        if(entity.getY() + entity.getHeight() > self.getWorldHeight()):
            entity.setY(self.getWorldHeight()-entity.getHeight())

        # check collision against world walls
        # top sensor
        tileTop = self.world.getTileAt(entity.getTopSensor())
        if(self.world.isWall(tileTop)):
            rect = self.world.getTileRect(tileTop)
            entity.setY(rect[1] + rect[3])

        # bottom sensor
        tileBottom = self.world.getTileAt(entity.getBottomSensor())
        if (self.world.isWall(tileBottom)):
            rect = self.world.getTileRect(tileBottom)
            entity.setY(rect[1]-entity.getHeight())

        # left sensor
        tileLeft = self.world.getTileAt(entity.getLeftSensor())
        if (self.world.isWall(tileLeft)):
            rect = self.world.getTileRect(tileLeft)
            entity.setX(rect[0] + rect[2])

        # right sensor
        tileRight = self.world.getTileAt(entity.getRightSensor())
        if (self.world.isWall(tileRight)):
            rect = self.world.getTileRect(tileLeft)
            entity.setX(rect[0] - entity.getWidth())


    def draw(self, screen) -> Simulation:
        self.world.draw(screen)
        for entity in self.entities:
            entity.draw(screen)

        return self

    def getWorldHeight(self):
        return self.world.getWorldHeight()

    def getWorldWidth(self):
        return self.world.getWorldWidth()


