import random
import time
from typing import TYPE_CHECKING

from src.AssetManager import AssetManager
from src.Entity.Entity import Entity
from src.Entity.HotSpot import HotSpot
from src.Math.Vector2D import Vector2D
from src.Simulation.Simulation import Simulation
from src.Walk.FollowHotSpotWalker import FollowHotSpotWalker
from src.Walk.RandomWalker import RandomWalker
from src.Walk.Walker import Walker

if TYPE_CHECKING:
    from src.Entity.Salesman import Salesman

class Consumer(Entity):
    MIN_TIME_BETWEEN_SELLS = 10 #secs

    wantsToBuy: bool
    nextWantToBuyCheck: int
    walker: Walker

    def __init__(self, simulation: Simulation, position: Vector2D, dimensions: Vector2D) -> None:
        super().__init__(simulation, position, dimensions)
        self.wantsToBuy = False
        self.nextWantToBuyCheck = int(round(time.time() * 1000))
        self.setWalker(RandomWalker())

    def loadAssets(self) -> None:
        self.setImage(AssetManager.getAsset("consumer"))

    def setWalker(self, walker: Walker) -> 'Consumer':
        self.walker = walker
        if(walker.getConsumer() != self):
            walker.setConsumer(self)
        return self

    def update(self):
        super().update()

        if isinstance(self.walker, RandomWalker):
            for entity in self.getEntitiesNearby():
                if isinstance(entity, HotSpot):
                    self.setWalker(FollowHotSpotWalker(entity))
        elif isinstance(self.walker, FollowHotSpotWalker) and self.walker.getHotspot() not in self.getEntitiesNearby():
            self.setWalker(RandomWalker())

        self.walker.walk()

    def getWalker(self) -> 'Walker':
        return self.walker

    def buy(self, seller: 'Salesman') -> bool:
        currentTime = int(round(time.time() * 1000))

        if(currentTime - self.nextWantToBuyCheck > 0):
            self.wantsToBuy = random.random() >= 0.6
            self.nextWantToBuyCheck = currentTime + self.MIN_TIME_BETWEEN_SELLS * 1000

        if(self.wantsToBuy == True):
            self.wantsToBuy = False
            return True
        else:
            return False



