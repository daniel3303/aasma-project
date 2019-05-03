import pygame


class AssetManager:
    loaded = False
    salesman = None
    consumer = None
    building = None


    @staticmethod
    def loadAssets():
        AssetManager.salesman = pygame.image.load("assets/salesman.png")
        AssetManager.consumer = pygame.image.load("assets/consumer.png")
        AssetManager.building = pygame.image.load("assets/building.png")

    @staticmethod
    def getAsset(asset: str):
        if(AssetManager.loaded == False):
            AssetManager.loadAssets()
        return getattr(AssetManager, asset)



