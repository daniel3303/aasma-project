from __future__ import annotations
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from src.Entity.Consumer import Consumer

class Walker:
    consumer: Consumer
    steps: int

    def __init__(self):
        self.consumer = None
        self.steps = 0

    def walk(self) -> None:
        self.steps += 1

    def setConsumer(self, entity: 'Consumer'):
        self.consumer = entity
        if(entity.getWalker() != self):
            entity.setWalker(self)

    def getConsumer(self) -> 'Consumer':
        return self.consumer

    def getSteps(self) -> int:
        return  self.steps

    def draw(self, screen):
        pass
