import random
import time
from typing import TYPE_CHECKING

from src.AssetManager import AssetManager
from src.Entity.Entity import Entity
from src.Math.Vector2D import Vector2D

if TYPE_CHECKING:
    from src.Simulation.Simulation import Simulation


class HotSpot(Entity):
    MAX_SHOW_TIME = 60
    MIN_SHOW_TIME = 20
    MAX_HIDE_TIME = 120
    MIN_HIDE_TIME = 40
    showSteps: int
    hideSteps: int

    def __init__(self, simulation: 'Simulation', position: Vector2D, dimensions: Vector2D) -> None:
        super().__init__(simulation, position, dimensions)
        self.setVelocity(Vector2D(0,0))

        self.setActive(random.randint(0, 1) == 1)
        self.showSteps = random.randint(self.MIN_SHOW_TIME, self.MAX_SHOW_TIME)
        self.hideSteps = random.randint(self.MIN_HIDE_TIME, self.MAX_HIDE_TIME)

    def loadAssets(self) -> None:
        self.setImage(AssetManager.getAsset("hotspot"))


    def update(self):
        super().update()

        if(self.isActive() and self.showSteps > 0):
            self.showSteps -= 1
        elif(self.isActive() and self.showSteps == 0):
            self.setActive(False)
        elif(not self.isActive() and self.hideSteps > 0):
            self.hideSteps -= 1
        elif(not self.isActive() and self.hideSteps == 0):
            self.setActive(True)
            self.showSteps = random.randint(self.MIN_SHOW_TIME, self.MAX_SHOW_TIME)
            self.hideSteps = random.randint(self.MIN_HIDE_TIME, self.MAX_HIDE_TIME)

    def draw(self, screen):
        if(not self.isActive()):
            return
        super().draw(screen)



