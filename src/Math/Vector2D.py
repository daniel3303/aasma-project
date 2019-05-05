from math import sqrt


class Vector2D:
    x: float
    y: float

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def getX(self) -> float:
        return self.x

    def getY(self) -> float:
        return self.y

    def set(self, vec: 'Vector2D') -> 'Vector2D':
        self.x = vec.getX()
        self.y = vec.getY()
        return self

    def setX(self, x: float) -> 'Vector2D':
        self.x = x
        return self

    def setY(self, y:float) -> 'Vector2D':
        self.y = y
        return self

    def sumX(self, val: float) -> 'Vector2D':
        self.x += val
        return self

    def sumY(self, val: float) -> 'Vector2D':
        self.y += val
        return self

    def norm(self) -> float:
        return sqrt(self.x**2 + self.y**2)

    def sum(self, vec: 'Vector2D'):
        self.x += vec.getX()
        self.y += vec.getY()

    def subtract(self, vec: 'Vector2D') -> 'Vector2D':
        self.x -= vec.getX()
        self.y -= vec.getY()
        return self

    def multiply(self, vec: 'Vector2D') -> 'Vector2D':
        self.x = self.x * vec.getX()
        self.y = self.y * vec.getY()
        return self

    def multiplyScalar(self, scalar: float) -> 'Vector2D':
        self.x = self.x * scalar
        self.y = self.y * scalar
        return self

    # Division by zero at user's care
    def divide(self, vec: 'Vector2D') -> 'Vector2D':
        self.x = self.x / vec.getX()
        self.y = self.y / vec.getY()
        return self

    # Division by zero at user's care
    def divideScalar(self, scalar: float) -> 'Vector2D':
        self.x = self.x / scalar
        self.y = self.y / scalar
        return self

    def dot(self, vec: 'Vector2D') -> float:
        return self.x * vec.getY() + self.y * vec.getY()

    def distanceTo(self, vec: 'Vector2D') -> float:
        selfCopy = self.copy()
        selfCopy.subtract(vec)
        return selfCopy.norm()

    def normalize(self) -> 'Vector2D':
        norm = self.norm()
        self.x = self.x / norm
        self.y = self.y /norm
        return self

    def equals(self, peer: 'Vector2D') -> bool:
        return self.getX() == peer.getX() and self.getY() == peer.getY()

    def copy(self) -> 'Vector2D':
        return Vector2D(self.x, self.y)
