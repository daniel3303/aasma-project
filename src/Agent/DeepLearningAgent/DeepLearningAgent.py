from __future__ import print_function, division
from builtins import range
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from datetime import datetime

from src.Agent.AbstractAgent import AbstractAgent
from src.Entity.Salesman import Salesman
from src.Entity.Consumer import Consumer


class DeepLearningAgent(AbstractAgent):
    nextAction: int

    def __init__(self, salesman: Salesman, model=None):
        super().__init__(salesman)
        salesman.setName("Deep Q Learning")
        self.nextAction = 0


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

        #print("Deciding: "+str(self.getCurrentActionName()))

        if self.nextAction == 0:
            salesman.moveRight()
        elif self.nextAction == 1:
            salesman.moveDown()
        elif self.nextAction == 2:
            salesman.moveLeft()
        elif self.nextAction == 3:
            salesman.moveUp()
        elif self.nextAction == 4:
            salesman.sell()
        else:
            print("ERROR: INVALID ACTION")

        print("sales: "+str(salesman.numSales)+" pos:"+str(salesman.getX())+","+str(salesman.getY())+" action: "+self.getCurrentActionName(), end="")

    def setNextAction(self, action: int) -> None:
        self.nextAction = action


    def getCurrentReward(self) -> float:
        return self.salesman.actionReward

    def getCurrentActionName(self) -> str:
        if self.nextAction == 0:
            return "right   "
        elif self.nextAction == 1:
            return  "down   "
        elif self.nextAction == 2:
            return "left    "
        elif self.nextAction == 3:
            return "up      "
        elif self.nextAction == 4:
            return "sell    "

        """
        1   1   0   0   0
        0   1   1   0   0
        1   0   0   1   0
        0   0   1   1   0
        
        """


    def getCurrentObservation(self):
        salesman = self.salesman
        entities = self.salesman.getSimulation().getEntities()

        # entities ordered by index
        entities = sorted(entities, key=lambda entity: entity.getId())

        observation = []

        # self position
        observation += [salesman.getX(), salesman.getY()]

        # other entities position
        for entity in entities:
            if isinstance(entity, Consumer):
                observation += [entity.getX(), entity.getX(), float(entity.getWantsToBuy())]

        return observation





# A version of HiddenLayer that keeps track of params
class HiddenLayer:
    def __init__(self, M1, M2, f=tf.nn.relu):
        self.W = tf.Variable(tf.random_normal(shape=(M1, M2)))
        self.W_other = tf.placeholder(dtype=tf.float32, shape=(M1, M2))

        self.copy_W_op = self.W.assign(self.W_other)
        self.params = [self.W]

        self.b = tf.Variable(np.zeros(M2).astype(np.float32))
        self.b_other = tf.placeholder(dtype=tf.float32, shape=(M2))
        self.params.append(self.b)
        self.copy_b_op = self.b.assign(self.b_other)
        self.f = f

    def forward(self, X):
        a = tf.matmul(X, self.W) + self.b
        return self.f(a)

    def copy_from(self, peer: 'HiddenLayer', session):
        peerW = session.run(peer.W)
        peerb = session.run(peer.b)
        session.run(self.copy_W_op, feed_dict={self.W_other: peerW})
        session.run(self.copy_b_op, feed_dict={self.b_other: peerb})



class DQN:
    def __init__(self, D, K, hidden_layer_sizes, gamma, max_experiences=100000, min_experiences=1000, batch_sz=512):
        self.K = K

        # create the graph
        self.layers = []

        M1 = D
        for M2 in hidden_layer_sizes:
            layer = HiddenLayer(M1, M2)
            self.layers.append(layer)
            M1 = M2

        # final layer linear
        layer = HiddenLayer(M1, K, lambda x: x)
        self.layers.append(layer)

        # collect params for copy
        self.params = []
        for layer in self.layers:
            self.params += layer.params

        # inputs and targets
        self.X = tf.placeholder(tf.float32, shape=(None, D), name='X')
        self.G = tf.placeholder(tf.float32, shape=(None,), name='G')
        self.actions = tf.placeholder(tf.int32, shape=(None,), name='actions')

        # calculate output and cost
        Z = self.X
        for layer in self.layers:
            Z = layer.forward(Z)
        Y_hat = Z
        self.predict_op = Y_hat

        selected_action_values = tf.reduce_sum(
            Y_hat * tf.one_hot(self.actions, K),
            axis=[1]
        )

        #selected_action_values = Y_hat * tf.one_hot(self.actions, K)

        self.cost = tf.square(self.G - selected_action_values)
        self.train_op = tf.train.AdamOptimizer(1e-2).minimize(self.cost)
        # self.train_op = tf.train.AdagradOptimizer(1e-2).minimize(self.cost)
        # self.train_op = tf.train.MomentumOptimizer(1e-3, momentum=0.9).minimize(self.cost)
        # self.train_op = tf.train.GradientDescentOptimizer(1e-4).minimize(self.cost)

        # create replay memory
        # state, action, reward, nextState, lastEpisodeState
        self.experience = {'s': [], 'a': [], 'r': [], 's2': []}
        self.max_experiences = max_experiences
        self.min_experiences = min_experiences
        self.batch_sz = batch_sz
        self.gamma = gamma


    def set_session(self, session):
        self.session = session

    def copy_from(self, other):
        for sl, pl in zip(self.layers, other.layers):
            sl.copy_from(pl, self.session)

    def predict(self, X):
        X = np.atleast_2d(X)
        return self.session.run(self.predict_op, feed_dict={self.X: X})

    def train(self, target_network):
        # sample a random batch from buffer, do an iteration of GD
        if len(self.experience['s']) < self.min_experiences:
            # don't do anything if we don't have enough experience
            return

        # randomly select a batch
        idx = np.random.choice(len(self.experience['s']), size=self.batch_sz, replace=False)
        states = [self.experience['s'][i] for i in idx]
        actions = [self.experience['a'][i] for i in idx]
        rewards = [self.experience['r'][i] for i in idx]
        next_states = [self.experience['s2'][i] for i in idx]
        next_Q = np.max(target_network.predict(next_states), axis=1)
        targets = [r + self.gamma * next_q for r, next_q in zip(rewards, next_Q)]

        """print("IN TRAIN")
        print("states: "+str(states))
        print("actions: "+str(actions))
        print("rewards: "+str(rewards))
        print("next states: "+str(next_states))
        print("next Q: "+str(next_Q))
        print("OUT TRAIN")"""


        # call optimizer
        cost, _ = self.session.run(
            [self.cost,
            self.train_op],
            feed_dict={
                self.X: states,
                self.G: targets,
                self.actions: actions
            }
        )

        print("cost: {0:08.2f} ".format(np.sum(cost)) + " ", end="")


    def add_experience(self, s, a, r, s2):
        if len(self.experience['s']) >= self.max_experiences:
            self.experience['s'].pop(0)
            self.experience['a'].pop(0)
            self.experience['r'].pop(0)
            self.experience['s2'].pop(0)
        self.experience['s'].append(s)
        self.experience['a'].append(a)
        self.experience['r'].append(r)
        self.experience['s2'].append(s2)

    def printExperience(self):
        for ind in range(len(self.experience["s"])-10, len(self.experience["s"])):
            print(str(self.experience["s"][ind]) + " | " + str(self.experience["a"][ind]) + " | " + str(self.experience["r"][ind]) + " | " + str(self.experience["s2"][ind]))

    def sample_action(self, x, eps):
        if np.random.random() < eps:
            return np.random.choice(self.K)
        else:
            X = np.atleast_2d(x)
            return np.argmax(self.predict(X)[0])

    def print_Q(self, x, target_nn):
        if len(self.experience['s']) < self.min_experiences:
            print("No experience")
            return

        X = np.atleast_2d(x)
        print(target_nn.predict(X))