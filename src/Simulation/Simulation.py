from __future__ import annotations

from src.Entity.Entity import Entity


class Simulation:
    entities: list[Entity]

    def __init__(self) -> None:
        self.entities = []
        pass

    def addEntity(self, entity: Entity) -> Simulation:
        self.entities.append(entity)
        return self

    def update(self, deltaTime: float) -> None:
        for entity in self.entities :
            entity.update(deltaTime)

    def draw(self, screen) -> Simulation:
        for entity in self.entities:
            entity.draw(screen)

        return self


