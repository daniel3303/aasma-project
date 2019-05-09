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
    MIN_STEPS_BETWEEN_SELLS = 240 #8 seconds at 30fps
    MAX_STEPS_BETWEEN_SELLS = 390 #13 seconds at 30fps

    wantsToBuy: bool
    stepsToUpdateBuyIntention: int
    walker: Walker

    def __init__(self, simulation: Simulation, position: Vector2D, dimensions: Vector2D) -> None:
        super().__init__(simulation, position, dimensions)
        self.wantsToBuy = False
        self.stepsToUpdateBuyIntention = 0
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
        self.updateBuyIntention()

    def getWalker(self) -> 'Walker':
        return self.walker

    def updateBuyIntention(self) -> None:
        self.stepsToUpdateBuyIntention -= 1

        if self.stepsToUpdateBuyIntention <= 0:
            self.wantsToBuy = random.random() >= 0.6
            self.stepsToUpdateBuyIntention = random.randint(Consumer.MIN_STEPS_BETWEEN_SELLS, Consumer.MAX_STEPS_BETWEEN_SELLS)

    def buy(self, seller: 'Salesman') -> bool:
        if(self.wantsToBuy == True):
            self.wantsToBuy = False
            return True

        return False

    def getWantsToBuy(self) -> bool:
        return self.wantsToBuy


