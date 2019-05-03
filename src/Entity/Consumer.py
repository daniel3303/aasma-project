from src.AssetManager import AssetManager
from src.Entity.Entity import Entity


class Consumer(Entity):

    def __init__(self, x: int, y: int, width: int, height: int, velocity: int) -> None:
        super().__init__(x, y, width, height, velocity)
        self.setImage(AssetManager.getAsset("consumer"))

