from __future__ import annotations

from math import sqrt
from random import randint
from typing import TYPE_CHECKING

import numpy as np
import pygame

from src.Walk.Walker import Walker

if TYPE_CHECKING:
    from src.Entity.Entity import Entity



class FollowWalker(Walker):
    target: Entity

    def __init__(self, target:Entity):
        super().__init__()
        self.target = target


    def walk(self):
        super().walk()
        entity = self.entity
        target = self.target

        vec = (target.getX() - entity.getX(), target.getY() - entity.getY())
        vecNorm = sqrt(vec[0]**2 + vec[1]**2)

        if(vecNorm < sqrt(entity.getWidth()**2 + entity.getHeight()**2)):
            return

        normalizedVec = (vec[0] / vecNorm, vec[1]/ vecNorm)

        movement = (normalizedVec[0] * entity.getVelocity(), normalizedVec[1] * entity.getVelocity())

        entity.moveX(movement[0])
        entity.moveY(movement[1])


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

    def draw(self, screen):
        pygame.draw.line(screen, (255, 0, 0), self.entity.getCenterOfMass(), self.target.getCenterOfMass(), 1)
