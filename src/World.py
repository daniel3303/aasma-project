import numpy as np
import pygame

from src.AssetManager import AssetManager
from src.Math.Vector2D import Vector2D
from src.Tile import Tile


class World():
    world: np.array([int])
    tileDimensions: Vector2D
    buildingImage: object

    def __init__(self):
        self.world = np.array([
            [1,1,1,1,1,1,1,1,1],
            [1,0,0,0,0,0,0,0,1],
            [1,0,1,0,1,0,1,0,1],
            [1,0,0,0,0,0,0,0,1],
            [1,0,1,0,1,0,1,0,1],
            [1,0,0,0,0,0,0,0,1],
            [1,1,1,1,1,1,1,1,1],
        ])

        self.tileDimensions = Vector2D(50,50)
        self.buildingImage = self.scaleTile(AssetManager.getAsset("building"))


    def getTileDimensions(self) -> Vector2D:
        return self.tileDimensions.copy()

    def getTileWidth(self) -> float:
        return self.tileDimensions.getX()

    def getTileHeight(self) -> float:
        return self.tileDimensions.getY()

    def getWorldDimensions(self) -> Vector2D:
        return Vector2D(self.getWorldWidth(), self.getWorldHeight())

    def getWorldWidth(self):
        return self.tileDimensions.getX() * self.world.shape[0]

    def getWorldHeight(self):
        return self.tileDimensions.getY() * self.world.shape[1]

    def scaleTile(self, image):
        return pygame.transform.scale(image, (self.getTileWidth(), self.getTileHeight()))

    def draw(self, screen):
        for tileX in range(0, self.world.shape[0]):
            for tileY in range(0, self.world.shape[1]):
                if(self.world[tileX][tileY] == 1):
                    screen.blit(self.buildingImage, (tileX*self.getTileWidth(), tileY*self.getTileHeight()))

    def getTileAt(self, position: Vector2D) -> 'Tile':
        tilePos = Vector2D(0,0)
        tilePos.setX(position.getX() // self.getTileWidth())
        tilePos.setY(position.getY() // self.getTileHeight())

        x = int(tilePos.getX())
        y = int(tilePos.getY())

        # check bounds
        if(x >= self.world.shape[0]):
            x = self.world.shape[0] - 1
        elif(x < 0):
            x = 0

        if (y >= self.world.shape[1]):
            y = self.world.shape[1] - 1
        elif (y < 0):
            y = 0

        isWall = self.world[x][y] != 0
        return Tile(tilePos, self.tileDimensions, isWall)