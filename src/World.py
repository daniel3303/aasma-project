import numpy as np
import pygame

from src.AssetManager import AssetManager


class World():
    world: np.array([int])
    tileWidth: int
    tileHeight: int
    buildingImage: object

    def __init__(self):
        self.world = np.array([
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        ])

        self.tileWidth = 30
        self.tileHeight = 30
        self.buildingImage = self.scaleTile(AssetManager.getAsset("building"))


    def getTileWidth(self) -> int:
        return self.tileWidth

    def getTileHeight(self) -> int:
        return self.tileHeight

    def getWorldWidth(self):
        return self.tileWidth * self.world.shape[0]

    def getWorldHeight(self):
        return self.tileHeight * self.world.shape[1]

    def scaleTile(self, image):
        return pygame.transform.scale(image, (self.getTileWidth(), self.getTileHeight()))

    def draw(self, screen):
        for tileX in range(0, self.world.shape[0]):
            for tileY in range(0, self.world.shape[1]):
                if(self.world[tileX][tileY] == 1):
                    screen.blit(self.buildingImage, (tileX*self.getTileWidth(), tileY*self.getTileHeight()))

    def getTileAt(self, tile) -> (int, int):
        return (int(tile[0] // self.getTileWidth()), int(tile[1] // self.getTileHeight()))

    def getTileRect(self, tile) -> (int, int, int, int):
        return (tile[0] * self.getTileWidth(), tile[1] * self.getTileHeight(), self.getTileWidth(), self.getTileHeight())

    def isWall(self, tile):
        return self.world[tile[0]][tile[1]] != 0