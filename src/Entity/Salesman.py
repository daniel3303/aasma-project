import random
import time
from typing import TYPE_CHECKING

import pygame

from src.AssetManager import AssetManager
from src.Entity.Entity import Entity
from src.Entity.HotSpot import HotSpot
from src.Math.Vector2D import Vector2D

if TYPE_CHECKING:
    from src.Entity.Consumer import Consumer
    from src.Simulation.Simulation import Simulation

class Salesman(Entity):
    SELL_SUCCESSED_REWARD = 1
    SELL_FAILED_REWARD = -0.03
    MOVING_REWARD = -0.005
    NOT_MOVING_REWARD = -0.001

    sales: ['Consumer']
    totalReward: float
    actionReward: float
    numSales: int


    actionMoveUp: bool
    actionMoveDown: bool
    actionMoveLeft: bool
    actionMoveRight: bool
    actionSell: bool
    actionSellTo: 'Consumer'

    name: str


    def __init__(self, simulation: 'Simulation', position: Vector2D, dimensions: Vector2D) -> None:
        super().__init__(simulation, position, dimensions)

        # Actions state
        self.actionMoveDown = False
        self.actionMoveLeft = False
        self.actionMoveUp = False
        self.actionMoveRight = False
        self.actionSell = False

        self.totalReward = 0.0
        self.actionReward = 0.0
        self.numSales = 0
        self.sales = []

        # A name for this entity
        self.name = "Salesman"

    def loadAssets(self) -> None:
        self.setImage(AssetManager.getAsset("salesman"))
        self.myfont = pygame.font.SysFont('Comic Sans MS', 22)

    def update(self):
        super().update() #does nothing
        self.actionReward = 0

        if self.actionSell:
            self.simulation.sell(self)

        if self.actionMoveUp:
            self.getVelocity().setX(0)
            self.getVelocity().setY(-self.maxVelocity)
            self.actionReward += self.MOVING_REWARD
        elif self.actionMoveDown:
            self.getVelocity().setX(0)
            self.getVelocity().setY(self.maxVelocity)
            self.actionReward += self.MOVING_REWARD
        elif self.actionMoveLeft:
            self.getVelocity().setX(-self.maxVelocity)
            self.getVelocity().setY(0)
            self.actionReward += self.MOVING_REWARD
        elif self.actionMoveRight:
            self.getVelocity().setX(self.maxVelocity)
            self.getVelocity().setY(0)
            self.actionReward += self.MOVING_REWARD
        else:
            self.actionReward += self.NOT_MOVING_REWARD

        # Updated the total reward based on the outcome of the last decisions
        self.totalReward += self.actionReward


        # Clear the action picked for this iteration
        self.resetActionState()

    def draw(self, screen):
        super().draw(screen)
        textsurface = self.myfont.render("{0:.2f}".format(self.totalReward), False, (255, 0, 0))
        screen.blit(textsurface, (self.getX()+self.getWidth(), self.getY() + self.getHeight()))


    def onSuccessSale(self, consumer) -> None:
        self.sales.append(consumer)
        self.numSales += 1
        self.actionReward += self.SELL_SUCCESSED_REWARD

    def onFailedSale(self, consumer) -> None:
        self.actionReward += self.SELL_FAILED_REWARD

    def resetActionState(self) -> None:
        self.actionMoveDown = False
        self.actionMoveLeft = False
        self.actionMoveUp = False
        self.actionMoveRight = False
        self.actionSell = False

    #### AVAILABLE ACTIONS ####
    def doNothing(self) -> None:
        self.resetActionState()

    def moveUp(self) -> None:
        self.actionMoveUp = True

    def moveDown(self) -> None:
        self.actionMoveDown = True

    def moveLeft(self) -> None:
        self.actionMoveLeft = True

    def moveRight(self) -> None:
        self.actionMoveRight = True

    # Tries to sell to the closest consumer
    def sell(self) -> None:
        self.actionSell = True


    ### AVAILABLE SENSORS ###

    # Returns the reward of the last action
    def getLastReward(self) -> float:
        return self.actionReward

    # Returns all the salesman nearby that we have vision to
    def getNearbySalesmen(self) -> ['Salesman']:
        entites = self.getEntitiesNearby()
        salesmen = []
        for entity in entites:
            if(isinstance(entity, Salesman)):
                salesmen.append(entity)

        return salesmen

    # Returns all the consumers nearby that we have vision to
    def getNearbyConsumers(self) -> ['Consumer']:
        from src.Entity.Consumer import Consumer
        entites = self.getEntitiesNearby()
        consumers = []
        for entity in entites:
            if (isinstance(entity, Consumer)):
                consumers.append(entity)

        return consumers

    # Returns all the hotspots nearby that we have vision to
    def getNearbyHotSpots(self) -> ['HotSpot']:
        entites = self.getEntitiesNearby()
        salesmen = []
        for entity in entites:
            if (isinstance(entity, HotSpot)):
                salesmen.append(entity)

        return salesmen

    def getTotalReward(self) -> float:
        return self.totalReward

    def getCurrentReward(self) -> float:
        return self.actionReward

    def setName(self, name: str):
        self.name = name

    def getName(self) -> str:
        return self.name

