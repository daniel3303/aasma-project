import random

from src.Agent.AbstractAgent import AbstractAgent
from src.Entity.Salesman import Salesman


class ReactiveAgent(AbstractAgent):
    walkCounter: int
    direction: str
    possibleDirections = [str]


    def __init__(self, salesman: Salesman):
        super().__init__(salesman)
        self.walkCounter = random.randint(1,20)
        self.possibleDirections = ["up", "down", "left", "right"]
        self.direction = random.choice(self.possibleDirections)



    # Decides which action to take next

    # Available actions:
    #   - moveUp
    #   - moveDown
    #   - moveLeft
    #   - moveRight
    #   - sellTo @param Consumer
    #   - doNoting

    # Available sensors
    #   getNearbySalesmen
    #   getNearbyConsumers
    #   getPosition
    #   getLastReward

    def decide(self):
        salesman = self.salesman

        self.walkCounter -= 1

        if self.direction == "down" :
            salesman.moveDown()
        elif self.direction == "up":
            salesman.moveUp()
        elif self.direction == "left":
            salesman.moveLeft()
        elif self.direction == "right":
            salesman.moveRight()

        # Always tries to sell to someone
        consumersNearBy = salesman.getNearbyConsumers()
        if consumersNearBy != []:
            consumer = random.choice(consumersNearBy)
            salesman.sellTo(consumer)

        # Updates the moving direction
        if self.walkCounter <= 0:
            self.updateDirection()


    def updateDirection(self):
        self.walkCounter = random.randint(1, 20)
        self.direction = random.choice(self.possibleDirections)


