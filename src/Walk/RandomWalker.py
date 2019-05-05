from __future__ import annotations
from random import randint
from typing import TYPE_CHECKING

from src.Math.Vector2D import Vector2D

import numpy as np
import pygame

from src.Walk.Walker import Walker

if TYPE_CHECKING:
    from src.Entity.Consumer import Consumer



class RandomWalker(Walker):
    lastPosition: Vector2D
    movement: np.array([int])
    remainingSteps: int


    def walk(self):
        super().walk()
        entity = self.consumer

        if(self.positionChanged() == False or self.remainingSteps <= 0):
            self.resetMovement()
            num = randint(0,3)
            self.movement[num] = 1
            self.movement = self.movement * entity.getMaxVelocity()
            self.remainingSteps = randint(0,200)
        else:
            self.remainingSteps -= 1

        direction = np.argmax(self.movement)
        if(direction == 0):
            self.consumer.setVelocity(Vector2D(self.movement[direction], 0))
        elif(direction == 1):
            self.consumer.setVelocity(Vector2D(-self.movement[direction], 0))
        elif(direction == 2):
            self.consumer.setVelocity(Vector2D(0, self.movement[direction]))
        elif(direction == 3):
            self.consumer.setVelocity(Vector2D(0, -self.movement[direction]))

    def setConsumer(self, consumer: 'Consumer'):
        super().setConsumer(consumer)
        self.lastPosition = consumer.getPosition()
        self.movement = np.array([0, 0, 0, 0])
        self.remainingSteps = 0

    def resetMovement(self):
        self.remainingSteps = 0
        self.movement = np.array([0,0,0,0])

    def positionChanged(self) -> bool:
        return not self.consumer.getPosition().equals(self.lastPosition)

