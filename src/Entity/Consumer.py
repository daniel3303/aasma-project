import random
import time

from src.AssetManager import AssetManager
from src.Entity.Entity import Entity


class Consumer(Entity):
    MIN_TIME_BETWEEN_SELLS = 10 #secs

    wantsToBuy: bool
    nextWantToBuyCheck: int

    def __init__(self, x: int, y: int, width: int, height: int, velocity: int) -> None:
        super().__init__(x, y, width, height, velocity)
        self.setImage(AssetManager.getAsset("consumer"))
        self.wantsToBuy = False
        self.nextWantToBuyCheck = int(round(time.time() * 1000))


    def getWantsToBuy(self) -> bool:
        currentTime = int(round(time.time() * 1000))

        if(currentTime - self.nextWantToBuyCheck > 0):
            self.wantsToBuy = random.random() >= 0.6
            self.nextWantToBuyCheck = currentTime + self.MIN_TIME_BETWEEN_SELLS * 1000

        if(self.wantsToBuy == True):
            self.wantsToBuy = False
            return True
        else:
            return False



