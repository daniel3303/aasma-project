import random
import time
from typing import TYPE_CHECKING

import pygame

from src.AssetManager import AssetManager
from src.Entity.Consumer import Consumer
from src.Entity.Entity import Entity
from src.Walk.FollowWalker import FollowWalker
from src.Walk.RandomWalker import RandomWalker


class Salesman(Entity):
    # state
    STATE_FOLLOWING = "STATE_FOLLOWING"

    SELL_VALUE = 1

    # properties
    lastTriesToSell: {Entity, int}
    sales: [Consumer]
    totalSold: int

    def __init__(self, x: int, y: int, width: int, height: int, velocity: int) -> None:
        super().__init__(x, y, width, height, velocity)
        self.setImage(AssetManager.getAsset("salesman"))
        self.sales = []
        self.totalSold = 0
        self.lastTriesToSell = {}

        self.myfont = pygame.font.SysFont('Comic Sans MS', 22)

    def update(self):
        super().update()
        if(self.walker != None and isinstance(self.walker, FollowWalker) and self.walker.getSteps() > 20):
            self.setWalker(RandomWalker())
            self.setState(self.STATE_WALKING)

        if(self.getState() == self.STATE_FOLLOWING and self.distanceTo(self.walker.target) <= self.velocity):
            sold = self.tryToSell(self.walker.target)
            if(sold):
                self.setState(self.STATE_WALKING)
                self.setWalker(RandomWalker())

    def sees(self, target:Entity) -> None:
        if(isinstance(target, Consumer) and self.getState() != self.STATE_FOLLOWING and self.triedToSellRecently(target) == False):
            self.setWalker(FollowWalker(target))
            self.setState(self.STATE_FOLLOWING)

    def dontSees(self, target: Entity):
        if(isinstance(target, Consumer) and target == self.isFollowing(target)):
            self.setWalker(RandomWalker())
            self.setState(RandomWalker)

    def addSale(self, consumer) -> None:
        self.sales.append(consumer)
        self.totalSold += self.SELL_VALUE

    def addTryToSell(self, consumer) -> None:
        self.lastTriesToSell[consumer] = int(round(time.time() * 1000))

    def isFollowing(self, target: Entity):
        return self.walker != None and isinstance(self.walker, FollowWalker) and self.walker.target == target

    def tryToSell(self, consumer) -> bool:
        sold = False
        if(consumer.getWantsToBuy()):
            self.onNewSale(consumer)
            sold = True
        self.addTryToSell(consumer)

        return sold

    def onNewSale(self, consumer):
        self.addSale(consumer)

    def triedToSellRecently(self, entity: Consumer):
        if(entity not in self.lastTriesToSell.keys()):
            return False

        val = self.lastTriesToSell[entity]
        currentTime = int(round(time.time() * 1000))

        if(val == None or val + entity.MIN_TIME_BETWEEN_SELLS * 1000 >= currentTime):
            return True
        else:
            return False

    def draw(self, screen):
        super().draw(screen)
        textsurface = self.myfont.render(str(self.totalSold), False, (255, 0, 0))
        screen.blit(textsurface, (self.getX()+self.getWidth(), self.getY() + self.getHeight()))










