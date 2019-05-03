from __future__ import annotations
from typing import TYPE_CHECKING

from src.Exception.MethodNotImplementedException import MethodNotImplementedException

if TYPE_CHECKING:
    from src.Entity.Entity import Entity


class Walker:
    entity: Entity
    steps: int

    def __init__(self):
        self.entity = None
        self.steps = 0

    def walk(self) -> None:
        self.steps += 1

    def setEntity(self, entity: Entity):
        self.entity = entity
        if(entity.getWalker() != self):
            entity.setWalker(self)

    def getEntity(self) -> Entity:
        return self.entity

    def getSteps(self) -> int:
        return  self.steps

    def draw(self, screen):
        pass
