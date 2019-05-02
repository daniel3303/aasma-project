class Entity:
    x: int
    y: int

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def getX(self) -> int:
        return self.x

