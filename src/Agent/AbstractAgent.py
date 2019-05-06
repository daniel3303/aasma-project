from src.Entity.Salesman import Salesman


class AbstractAgent:
    # The controlled salesman
    salesman: Salesman

    def __init__(self, salesman: Salesman):
        self.salesman = salesman

    # Called whenever the agent must choose an action

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
        pass





