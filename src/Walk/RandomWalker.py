from __future__ import annotations
from random import randint
from typing import TYPE_CHECKING

import numpy as np

from src.Walk.Walker import Walker

if TYPE_CHECKING:
    from src.Entity.Entity import Entity



class RandomWalker(Walker):
    lastX: int
    lastY: int
    movement: np.array([int])
    remainingSteps: int


    def walk(self):
        super().walk()
        entity = self.entity

        if(self.positionChanged() == False or self.remainingSteps <= 0):
            self.resetMovement()
            num = randint(0,3)
            self.movement[num] = 1
            self.movement = self.movement * entity.getVelocity()
            self.remainingSteps = randint(0,200)
        else:
            self.remainingSteps -= entity.getVelocity()

        direction = np.argmax(self.movement)
        if(direction == 0):
            self.entity.moveX(self.movement[direction])
        elif(direction == 1):
            self.entity.moveX(-self.movement[direction])
        elif(direction == 2):
            self.entity.moveY(self.movement[direction])
        elif(direction == 3):
            self.entity.moveY(-self.movement[direction])

    def setEntity(self, entity: Entity):
        super().setEntity(entity)
        self.lastX = entity.getX()
        self.lastY = entity.getY()
        self.movement = np.array([0, 0, 0, 0])
        self.remainingSteps = 0

    def resetMovement(self):
        self.remainingSteps = 0
        self.movement = np.array([0,0,0,0])

    def positionChanged(self):
        return self.entity.getX() != self.lastX or self.entity.getY() != self.lastY
