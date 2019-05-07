from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

from src.Math.Vector2D import Vector2D

if TYPE_CHECKING:
    from src.Simulation.Simulation import Simulation


class Entity:
    ID = 0
    MAX_VELOCITY = 20
    VIEW_RANGE = 300

    # unique entity identifier
    id: int
    simulation: Simulation
    position: Vector2D
    velocity: Vector2D
    dimensions: Vector2D
    image: pygame.Surface
    viewRange: float
    state: str
    entitiesNearBy: [Entity]
    maxVelocity: float
    active: bool
    assetsLoaded: bool

    def __init__(self, simulation: Simulation, position: Vector2D, dimensions: Vector2D) -> None:
        self.id = Entity.ID = Entity.ID + 1 # entity unique ID
        self.active = True
        self.simulation = simulation
        self.position = position.copy()
        self.dimensions = dimensions.copy()
        self.velocity = Vector2D(0,0)
        self.maxVelocity = Entity.MAX_VELOCITY

        self.assetsLoaded = False
        self.image = None
        self.viewRange = self.VIEW_RANGE
        self.entitiesNearBy = []

    def getId(self) -> int:
        return self.id

    def setImage(self, image):
        self.image = pygame.transform.scale(image, (self.getWidth(), self.getHeight()))

    def getPosition(self) -> 'Vector2D':
        return self.position.copy()

    def setPosition(self, position: 'Vector2D') -> Entity:
        self.position = position
        return self

    def getX(self) -> float:
        return self.position.getX()

    def getY(self) -> float:
        return self.position.getY()

    def getDimensions(self) -> 'Vector2D':
        return self.dimensions.copy()

    def getWidth(self) -> float:
        return self.dimensions.getX()

    def getHeight(self) -> float:
        return self.dimensions.getY()

    def getVelocity(self) -> 'Vector2D':
        return self.velocity

    def setVelocity(self, velocity: 'Vector2D') -> Entity:
        self.velocity = velocity.copy()
        return self

    def getMaxVelocity(self) -> float:
        return self.maxVelocity

    def getTopSensor(self) -> 'Vector2D':
        sensor = self.position.copy()
        return sensor.sumX(self.getWidth() / 2)

    def getBottomSensor(self) -> 'Vector2D':
        sensor = self.getTopSensor()
        return sensor.sumY(self.getHeight())

    def getLeftSensor(self) -> 'Vector2D':
        sensor = self.position.copy()
        return sensor.sumY(self.getHeight() / 2)

    def getRightSensor(self) -> 'Vector2D':
        sensor = self.getLeftSensor()
        return sensor.sumX(self.getWidth())

    def getCenterOfMass(self) -> 'Vector2D':
        sensor = self.getPosition()
        sensor.sum(self.getDimensions().divideScalar(2))
        return sensor

    def setX(self, x: float) -> Entity:
        self.position.setX(x)
        return self

    def setY(self, y: float) -> Entity:
        self.position.setY(y)
        return self

    def getRect(self):
        return pygame.Rect(self.getX(), self.getY(), self.getWidth(), self.getHeight())

    def getViewRange(self) -> float:
        return self.viewRange

    def getSimulation(self) -> Simulation:
        return self.simulation

    def update(self) -> Entity:
        self.position.sum(self.velocity)
        return self

    def loadAssets(self) -> None:
        pass

    def draw(self, screen) -> Entity:
        if not self.assetsLoaded:
            self.loadAssets()
            self.assetsLoaded = True

        if(self.image != None):
            screen.blit(self.image, (self.getX(), self.getY()))
        else:
            pygame.draw.rect(screen, (255, 0, 0), (self.getX(), self.getY(), self.getWidth(), self.getHeight()))
        return self

    def setActive(self, active: bool) -> Entity:
        self.active = active
        return self

    def isActive(self) -> bool:
        return self.active

    def distanceTo(self, entity: Entity) -> float:
        return self.getCenterOfMass().distanceTo(entity.getCenterOfMass())

    def setEntitiesNearBy(self, entities: [Entity]) -> None:
        self.entitiesNearBy = entities

    def getEntitiesNearby(self) -> [Entity]:
        return self.entitiesNearBy


