import numpy as np
import pygame

from src.AssetManager import AssetManager
from src.Math.Vector2D import Vector2D


class Tile():
    position: Vector2D
    wall: bool

    def __init__(self, position: Vector2D, dimensions: Vector2D, isWall: bool):
        self.position = position
        self.dimensions = dimensions
        self.wall = isWall

    def getPostion(self) -> 'Vector2D':
        return self.position.copy()

    def getX(self) -> float:
        return self.position.getX()

    def getY(self) -> float:
        return self.position.getY()

    def getWorldX(self) -> float:
        return self.position.getX() * self.getWidth()

    def getWorldY(self) -> float:
        return self.position.getY() * self.getHeight()

    def getWorldPosition(self) -> 'Vector2D':
        return Vector2D(self.getWorldX(), self.getWorldY())

    def getDimensions(self) -> 'Vector2D':
        return self.dimensions.copy()

    def getWidth(self) -> float:
        return self.dimensions.getX()

    def getHeight(self) -> float:
        return self.dimensions.getY()

    def isWall(self) -> bool:
        return self.wall

