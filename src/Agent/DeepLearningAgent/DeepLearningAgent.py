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
        self.nextAction = np.random.randint(0, 5)

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

        print("sales: " + str(salesman.numSales) + " pos:" + str(salesman.getX()) + "," + str(
            salesman.getY()) + " action: " + self.getCurrentActionName(), end="")

    def setNextAction(self, action: int) -> None:
        self.nextAction = action

    def getCurrentReward(self) -> float:
        return self.salesman.actionReward

    def getCurrentActionName(self) -> str:
        if self.nextAction == 0:
            return "right   "
        elif self.nextAction == 1:
            return "down   "
        elif self.nextAction == 2:
            return "left    "
        elif self.nextAction == 3:
            return "up      "
        elif self.nextAction == 4:
            return "sell    "

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
                observation += [entity.getX(), entity.getX(), float(entity.getWasRecentlyAskedToBuy())]

        return observation


class HiddenLayer:
    def __init__(self, M1, M2, f=tf.nn.tanh):
        self.W = tf.Variable(tf.random_normal(shape=(M1, M2)))
        self.b = tf.Variable(np.zeros(M2).astype(np.float32))
        self.f = f

    def forward(self, X):
        a = tf.matmul(X, self.W) + self.b
        return self.f(a)


class DQN:
    def __init__(self, D, K, hidden_layer_sizes, gamma, max_experiences=50000, min_experiences=10, batch_sz=2):
        # input nodes
        self.D = D

        # output nodes
        self.K = K

        # create the graph
        self.layers = []

        M1 = D
        for M2 in hidden_layer_sizes:
            layer = HiddenLayer(M1, M2)
            self.layers.append(layer)
            M1 = M2

        # the final layer is linear
        layer = HiddenLayer(M1, K, lambda x: x)
        self.layers.append(layer)

        # input state
        self.X = tf.placeholder(tf.float32, shape=(None, D), name='X')

        # G matrix
        self.G = tf.placeholder(tf.float32, shape=(None,), name='G')

        # action taken
        self.actions = tf.placeholder(tf.int32, shape=(None,), name='actions')

        # calculate output and cost
        Z = self.X
        for layer in self.layers:
            Z = layer.forward(Z)
        Y_hat = Z
        self.predict_op = Y_hat

        # Q value for the actions taken
        self.selected_action_values = selected_action_values = tf.reduce_sum(
            Y_hat * tf.one_hot(self.actions, K),
            axis=[1]
        )

        # mean squared error for cost function
        self.cost = tf.reduce_sum(tf.square(self.G - selected_action_values))
        self.train_op = tf.train.AdamOptimizer(1e-2).minimize(self.cost)
        # self.train_op = tf.train.AdagradOptimizer(1e-2).minimize(self.cost)
        # self.train_op = tf.train.MomentumOptimizer(1e-3, momentum=0.9).minimize(self.cost)
        # self.train_op = tf.train.GradientDescentOptimizer(1e-4).minimize(self.cost)

        # create replay memory
        # state, action, reward, nextState, episodeLast?
        self.experience = {'s': [], 'a': [], 'r': [], 's2': [], 'done': []}
        self.max_experiences = max_experiences
        self.min_experiences = min_experiences
        self.batch_sz = batch_sz
        self.gamma = gamma

    def set_session(self, session):
        self.session = session

    def predict(self, X):
        X = np.atleast_2d(X)
        return self.session.run(self.predict_op, feed_dict={self.X: X})

    def train(self):
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
        dones = [self.experience['done'][i] for i in idx]

        next_Q = np.max(self.predict(next_states), axis=1)
        targets = [r + self.gamma * next_q if not done else r for r, next_q, done in zip(rewards, next_Q, dones)]

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

        print("cost: {0:07.2f} ".format(cost) + " ", end="")

    def add_experience(self, s, a, r, s2, done):
        if len(self.experience['s']) >= self.max_experiences:
            self.experience['s'].pop(0)
            self.experience['a'].pop(0)
            self.experience['r'].pop(0)
            self.experience['s2'].pop(0)
            self.experience['done'].pop(0)
        self.experience['s'].append(s)
        self.experience['a'].append(a)
        self.experience['r'].append(r)
        self.experience['s2'].append(s2)
        self.experience['done'].append(done)

    def sample_action(self, x, eps):
        if np.random.random() < eps:
            return np.random.choice(self.K)
        else:
            X = np.atleast_2d(x)
            return np.argmax(self.predict(X)[0])


def save_model(session, model, modelName):
    file = "models/" + modelName + ".npy"
    params = model.params
    actual = []
    for p in params:
        v = session.run(p)
        actual.append(v)
    np.save(file, actual)


def load_modal(session, model, modelName):
    file = "models/" + modelName + ".npy"
    savedParams = np.load(file, allow_pickle=True)
    myParams = model.params
    ops = []
    for m, s in zip(myParams, savedParams):
        op = m.assign(s)
        ops.append(op)
    # now run them all
    session.run(ops)
