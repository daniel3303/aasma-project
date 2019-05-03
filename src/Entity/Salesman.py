import random
from typing import TYPE_CHECKING

from src.AssetManager import AssetManager
from src.Entity.Consumer import Consumer
from src.Entity.Entity import Entity
from src.Walk.FollowWalker import FollowWalker
from src.Walk.RandomWalker import RandomWalker


class Salesman(Entity):

    def __init__(self, x: int, y: int, width: int, height: int, velocity: int) -> None:
        super().__init__(x, y, width, height, velocity)
        self.setImage(AssetManager.getAsset("salesman"))

    def update(self):
        super().update()
        if(self.walker != None and isinstance(self.walker, FollowWalker) and self.walker.getSteps() > 20):
            self.setWalker(RandomWalker())

    def sees(self, target:Entity) -> None:
        if(isinstance(target, Consumer)):
            self.setWalker(FollowWalker(target))

    def dontSees(self, target: Entity):
        if(isinstance(target, Consumer) and target == self.isFollowing(target)):
            self.setWalker(RandomWalker())

    def isFollowing(self, target: Entity):
        return self.walker != None and isinstance(self.walker, FollowWalker) and self.walker.target == target





