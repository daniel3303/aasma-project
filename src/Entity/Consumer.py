from src.Entity.Entity import Entity


class Consumer(Entity):

    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y)

