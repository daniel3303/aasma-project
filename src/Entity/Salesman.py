import random
import time
from typing import TYPE_CHECKING

import pygame

from src.AssetManager import AssetManager
from src.Entity.Consumer import Consumer
from src.Entity.Entity import Entity
from src.Simulation.Simulation import Simulation


class Salesman(Entity):
    SELL_SUCCESSED_REWARD = 1
    SELL_FAILED_REWARD = 0
    MOVING_REWARD = -0.005
    NOT_MOVING_REWARD = 0

    sales: [Consumer]
    totalReward: float
    actionReward: float
    numSales: int


    actionMoveUp: bool
    actionMoveDown: bool
    actionMoveLeft: bool
    actionMoveRight: bool
    actionSell: bool
    actionSellTo: Consumer


    def __init__(self, simulation: Simulation, x: int, y: int, width: int, height: int, velocity: int) -> None:
        super().__init__(simulation, x, y, width, height, velocity)

        # Actions state
        self.actionMoveDown = False
        self.actionMoveLeft = False
        self.actionMoveUp = False
        self.actionMoveRight = False
        self.actionSell = False
        self.actionSellTo = None

        self.totalReward = 0.0
        self.actionReward = 0.0
        self.numSales = 0
        self.sales = []

        self.setImage(AssetManager.getAsset("salesman"))
        self.myfont = pygame.font.SysFont('Comic Sans MS', 22)

    def update(self):
        super().update()
        self.actionReward = 0

        if self.actionSell:
            self.simulation.sell(self, self.actionSellTo)
        if self.actionMoveUp:
            self.moveY(-self.velocity)
            self.actionReward += self.MOVING_REWARD
        elif self.actionMoveDown:
            self.moveY(self.velocity)
            self.actionReward += self.MOVING_REWARD
        elif self.actionMoveLeft:
            self.moveX(-self.velocity)
            self.actionReward += self.MOVING_REWARD
        elif self.actionMoveRight:
            self.moveX(self.velocity)
            self.actionReward += self.MOVING_REWARD
        else:
            self.actionReward += self.NOT_MOVING_REWARD

    def draw(self, screen):
        super().draw(screen)
        textsurface = self.myfont.render(str(self.totalReward), False, (255, 0, 0))
        screen.blit(textsurface, (self.getX()+self.getWidth(), self.getY() + self.getHeight()))


    def addSuccessSale(self, consumer) -> None:
        self.sales.append(consumer)
        self.totalReward += self.SELL_SUCCESSED_REWARD
        self.numSales += 1
        self.actionReward += self.SELL_SUCCESSED_REWARD

    def addFailedSale(self, consumer) -> None:
        self.totalReward += self.SELL_FAILED_REWARD
        pass

    def resetActionState(self) -> None:
        self.actionMoveDown = False
        self.actionMoveLeft = False
        self.actionMoveUp = False
        self.actionMoveRight = False
        self.actionSell = False

    #### AVAILABLE ACTIONS ####
    def doNothing(self) -> None:
        pass

    def moveUp(self) -> None:
        self.actionMoveUp = True

    def moveDown(self) -> None:
        self.actionMoveDown = True

    def moveLeft(self) -> None:
        self.actionMoveLeft = True

    def moveRight(self) -> None:
        self.actionMoveRight = True

    def sell(self, consumer: Consumer) -> None:
        self.actionSell = True
        self.actionSellTo = consumer


    ### AVAILABLE SENSORS ###

    # Returns the reward of the last action
    def getReward(self) -> float:
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
        entites = self.getEntitiesNearby()
        consumers = []
        for entity in entites:
            if (isinstance(entity, Salesman)):
                consumers.append(entity)

        return consumers

