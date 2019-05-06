from __future__ import annotations
from random import randint
from typing import TYPE_CHECKING

from src.Entity.HotSpot import HotSpot
from src.Math.Vector2D import Vector2D

import numpy as np
import pygame

from src.Walk.Walker import Walker

if TYPE_CHECKING:
    from src.Entity.Consumer import Consumer



class FollowHotSpotWalker(Walker):
    hotspot: HotSpot
    minHotSpotDistance: float

    def __init__(self, hotspot: HotSpot):
        super().__init__()
        self.hotspot = hotspot
        self.minHotSpotDistance = randint(1, int(self.hotspot.getSimulation().getTileWidth()*1.5))

    def walk(self):
        super().walk()
        if self.consumer is None:
            return

        entity = self.consumer
        hotspot = self.hotspot

        direction = hotspot.getPosition().subtract(entity.getPosition())

        # we must prevent norm 0 vec and all users at exacly the same spot
        if(direction.norm() < self.minHotSpotDistance):
            self.consumer.setVelocity(Vector2D(0,0))
            return

        direction.normalize().multiplyScalar(entity.getMaxVelocity())

        self.consumer.setVelocity(direction)

    def setConsumer(self, consumer: 'Consumer'):
        super().setConsumer(consumer)

    def getHotspot(self) -> 'HotSpot':
        return self.hotspot

