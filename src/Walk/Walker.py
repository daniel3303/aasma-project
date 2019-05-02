from __future__ import annotations
from typing import TYPE_CHECKING

from src.Exception.MethodNotImplementedException import MethodNotImplementedException

if TYPE_CHECKING:
    from src.Entity.Entity import Entity


class Walker:
    entity: Entity

    def __init__(self):
        self.entity = None

    def walk(self, deltaTime: int) -> None:
        raise MethodNotImplementedException("Not implemented")

    def setEntity(self, entity: Entity):
        self.entity = entity
        if(entity.getWalker() != self):
            entity.setWalker(self)

    def getEntity(self) -> Entity:
        return self.entity
