from __future__ import annotations

from math import sqrt
from random import randint
from typing import TYPE_CHECKING

from src.Agent.AbstractAgent import AbstractAgent

if(TYPE_CHECKING):
    from src.Entity.Salesman import Salesman
    from src.Entity.Entity import Entity
    from src.Entity.Consumer import Consumer

from src.World import World


class Simulation:
    MAX_DISTANCE_TO_ALLOW_SELL = 60

    # The entities belonging to the world
    entities: [Entity]

    # The agents that control the entities
    agents: [AbstractAgent]

    # The world instance
    world: World

    def __init__(self, world: World) -> None:
        self.entities = []
        self.agents = []
        self.world = world
        pass

    def addEntity(self, entity: Entity) -> Simulation:
        # prevents adding the same entity multiple times
        if(entity in self.entities):
            return self
        self.entities.append(entity)
        return self

    def removeEntity(self, entity: Entity) -> Simulation:
        self.entities.remove(entity)
        return self

    def addAgent(self, agent: AbstractAgent) -> Simulation:
        # prevents adding the same entity multiple times
        if(agent in self.agents):
            return self
        self.agents.append(agent)
        return self

    def removeAgent(self, agent: AbstractAgent) -> Simulation:
        self.agents.remove(agent)
        return self

    def update(self) -> None:
        for agent in self.agents:
            agent.decide()

        for entity in self.entities:
            entity.update()
            self.forceInBound(entity)

        # check entities contact
        for entity in self.entities:
            # dont check contact for inactive entities
            if not entity.isActive():
                continue

            viewableEntities = []
            for target in self.entities:
                if entity != target and target.isActive():
                    if self.entityCanView(entity, target):
                        viewableEntities.append(target)
            entity.setEntitiesNearBy(viewableEntities)

    def sell(self, seller: Salesman, buyer: Consumer):
        if(self.distanceBetween(seller, buyer) <= self.MAX_DISTANCE_TO_ALLOW_SELL):
            wantsToBuy = buyer.buy(seller)
            if(wantsToBuy):
                seller.onSuccessSale(buyer)
            else:
                seller.onFailedSale(buyer)


    # Checks whenever entity A can see entity B in the map
    def entityCanView(self, a: Entity, b: Entity) -> bool:
        vec = b.getCenterOfMass().subtract(a.getCenterOfMass())
        vecLen = vec.norm()
        if(vecLen == 0):
            return True
        elif(vecLen > a.getViewRange()):
            return False

        totalSteps = int(vecLen)

        normalizedVec = vec.copy().normalize()

        aPos = a.getCenterOfMass()
        for step in range(0, totalSteps):
            aPos.sum(normalizedVec)

            tile = self.world.getTileAt(aPos)
            if(tile.isWall()):
                return False

        return True

    # Returns the distance between two entities
    def distanceBetween(self, a: Entity, b: Entity) -> float:
        return sqrt(((a.getX() - b.getX())**2 + (a.getY() - b.getY())**2))


    # Force an entity to stay in the map free to walk zone
    def forceInBound(self, entity: Entity) -> None:
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
        if(tileTop.isWall()):
            newY = tileTop.getWorldY() + tileTop.getHeight()
            entity.setY(newY)


        # bottom sensor
        tileBottom = self.world.getTileAt(entity.getBottomSensor())
        if (tileBottom.isWall()):
            newY = tileBottom.getWorldY() - entity.getHeight()
            entity.setY(newY)

        # left sensor
        tileLeft = self.world.getTileAt(entity.getLeftSensor())
        if (tileLeft.isWall()):
            newX = tileLeft.getWorldX() + tileLeft.getWidth()
            entity.setX(newX)

        # right sensor
        tileRight = self.world.getTileAt(entity.getRightSensor())
        if (tileRight.isWall()):
            newX = tileRight.getWorldX() - entity.getWidth()
            entity.setX(newX)


    # Draws the simulation
    def draw(self, screen) -> Simulation:
        self.world.draw(screen)
        for entity in self.entities:
            entity.draw(screen)

        return self


    # Returns the height of the world
    def getWorldHeight(self) -> int:
        return self.world.getWorldHeight()


    # Returns the width of the world
    def getWorldWidth(self) -> int:
        return self.world.getWorldWidth()

    def getTileWidth(self) -> float:
        return self.world.getTileWidth()

    def getTileHeight(self) -> float:
        return self.world.getTileHeight()


