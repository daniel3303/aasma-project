import random
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
    MIN_STEPS_BETWEEN_SELLS = 300 #10 seconds at 30fps

    wantsToBuy: bool
    stepsSinceLastSellingAttempt: int
    walker: Walker

    def __init__(self, simulation: Simulation, position: Vector2D, dimensions: Vector2D) -> None:
        super().__init__(simulation, position, dimensions)
        self.wantsToBuy = False
        self.stepsSinceLastSellingAttempt = 0
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
        self.stepsSinceLastSellingAttempt += 1

    def getWalker(self) -> 'Walker':
        return self.walker

    def buy(self, seller: 'Salesman') -> bool:
        if(self.stepsSinceLastSellingAttempt / Consumer.MIN_STEPS_BETWEEN_SELLS >= 1):
            self.wantsToBuy = random.random() >= 0.6
            self.stepsSinceLastSellingAttempt = 0

        if(self.wantsToBuy == True):
            self.wantsToBuy = False
            self.stepsSinceLastSellingAttempt = 0
            return True
        else:
            return False

    def getNumStepsSinceLastSellingAttempt(self) -> int:
        return self.stepsSinceLastSellingAttempt


