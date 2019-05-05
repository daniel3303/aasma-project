import pygame


class AssetManager:
    loaded = False
    salesman = None
    consumer = None
    building = None
    hotspot = None


    @staticmethod
    def loadAssets():
        AssetManager.salesman = pygame.image.load("assets/salesman.png")
        AssetManager.consumer = pygame.image.load("assets/consumer.png")
        AssetManager.building = pygame.image.load("assets/building.png")
        AssetManager.hotspot = pygame.image.load("assets/hotspot.png")

    @staticmethod
    def getAsset(asset: str):
        if(AssetManager.loaded == False):
            AssetManager.loadAssets()
        return getattr(AssetManager, asset)



