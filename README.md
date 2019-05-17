# AASMA Project
Project for the AASMA course.
Group 49

| Student Number | Name |
|----------------|-------|
|83450|Duarte De Matos Soeiro Correia Teles|
|87848|Daniel Alexandre Pratas de Oliveira|

# Requirements
This game requires python 3.7 (due to the strong type-checking used in the code). Python 4 works as well.
Besides that other libraries like pygame are required. Run the following commands to install all dependencies.

    pip install pygame
    pip install tensorflow
    pip install numpy
    pip install matplotlib


# Game Preview
This game consists of the salesman problem. Several salesman represented by the icon of a huy with a dark background try to sell products to the consumers, represented by the guys with a green backgound.

![Game Screenshot](https://github.com/daniel3303/aasma-project/raw/master/screenshot.png)

# Utility function
The following utility function is used to calculate each salesman score:

| Description | Value |
| ----------- | ----- |
| Success sale | 100 |
| Failed sale | -1 |

You can change the utility function to train your own model. To do so you need to change the `src\Entity|Saleman.py` file. The following options are available:


| Name | Description |
| ----------- | ----- |
| SELL_SUCCESSED_REWARD | Reward given when the agent completes a sale with success |
| SELL_FAILED_REWARD | Reward given when the agent fails to sell |
| MOVING_REWARD | Reward given when the agent moves. If he tries to move against a wall this reward is not given |
| DO_NOTHING_REWARD | Reward given when the agent does not choose any action |
| NOT_MOVING_REWARD | Reward given if the agent does not move or move against a wall. You may want to use a negative value here to encorauge the agent to keep moving around. |

    
# Training
This repository cames with a pre-trained model for the problem. This model is however not the best since it was trained over only 136 game episodes. You may want to train your own model. To do so run the following command:

    python train.py
    
# Running
To run the game using the current pre-trained model run the following command:

    python run.py
    

    
