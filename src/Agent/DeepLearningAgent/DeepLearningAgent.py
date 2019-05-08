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
    modelName: str
    training: bool

    def __init__(self, salesman: Salesman, model=None):
        super().__init__(salesman)
        salesman.setName("Deep Q Learning")
        self.nextAction = 0
        self.modelName = model
        self.training = True

        if self.modelName:
            self.training = False
            gamma = 0.99
            D = 38  # fix me make it dynamic
            K = 5  # fix me make it dynamic

            sizes = [200, 300, 200]
            self.model = model = DQN(D, K, sizes, gamma)
            session = tf.InteractiveSession()
            init = tf.global_variables_initializer()
            session.run(init)
            model.set_session(session)
            load_modal(session, model, self.modelName)


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


        if self.modelName:
            self.nextAction = self.model.sample_action(self.getCurrentObservation(), 0.1)


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

        print("pos:"+str(salesman.getX())+","+str(salesman.getY())+" action: "+self.getCurrentActionName(), end="")

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
            observation += [entity.getX(), entity.getX()]
            if isinstance(entity, Consumer):
                observation += [float(entity.getWasRecentlyAskedToBuy())]

        return observation





# A version of HiddenLayer that keeps track of params
class HiddenLayer:
    def __init__(self, M1, M2, f=tf.nn.leaky_relu, use_bias=True):
        self.W = tf.Variable(tf.random_normal(shape=(M1, M2)))
        self.params = [self.W]
        self.use_bias = use_bias
        if use_bias:
            self.b = tf.Variable(np.zeros(M2).astype(np.float32))
            self.params.append(self.b)
        self.f = f

    def forward(self, X):
        if self.use_bias:
            a = tf.matmul(X, self.W) + self.b
        else:
            a = tf.matmul(X, self.W)
        return self.f(a)


class DQN:
    def __init__(self, D, K, hidden_layer_sizes, gamma, max_experiences=6000, min_experiences=100, batch_sz=32):
        self.K = K

        # create the graph
        self.layers = []

        # first layer linear
        layer = HiddenLayer(D, hidden_layer_sizes[1])
        self.layers.append(layer)
        M1 = hidden_layer_sizes[1]


        for M2 in hidden_layer_sizes[1:]:
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

        cost = tf.reduce_sum(tf.square(self.G - selected_action_values))
        self.train_op = tf.train.AdamOptimizer(1e-2).minimize(cost)
        # self.train_op = tf.train.AdagradOptimizer(1e-2).minimize(cost)
        # self.train_op = tf.train.MomentumOptimizer(1e-3, momentum=0.9).minimize(cost)
        # self.train_op = tf.train.GradientDescentOptimizer(1e-4).minimize(cost)

        # create replay memory
        # state, action, reward, nextState, lastEpisodeState
        self.experience = {'s': [], 'a': [], 'r': [], 's2': [], 'done': []}
        self.max_experiences = max_experiences
        self.min_experiences = min_experiences
        self.batch_sz = batch_sz
        self.gamma = gamma

    def set_session(self, session):
        self.session = session

    def copy_from(self, other):
        # collect all the ops
        ops = []
        my_params = self.params
        other_params = other.params
        for p, q in zip(my_params, other_params):
            actual = self.session.run(q)
            op = p.assign(actual)
            ops.append(op)
        # now run them all
        self.session.run(ops)

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
        # print("idx:", idx)
        states = [self.experience['s'][i] for i in idx]
        actions = [self.experience['a'][i] for i in idx]
        rewards = [self.experience['r'][i] for i in idx]
        next_states = [self.experience['s2'][i] for i in idx]
        dones = [self.experience['done'][i] for i in idx]
        next_Q = np.max(target_network.predict(next_states), axis=1)
        targets = [r + self.gamma * next_q if not done else r for r, next_q, done in zip(rewards, next_Q, dones)]

        # call optimizer
        self.session.run(
            self.train_op,
            feed_dict={
                self.X: states,
                self.G: targets,
                self.actions: actions
            }
        )

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
    file = "models/"+modelName+".npy"
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




