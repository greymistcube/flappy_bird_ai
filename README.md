# Flappy Bird with NEAT

This project was inspired by [this paper.]
(http://nn.cs.utexas.edu/downloads/papers/stanley.ec02.pdf) This is my own
take on neuroevolution borrowing many ideas presented in the paper.
This is just the first small project for implementing the idea from scratch,
and not everything is implemented to its full extent. Its possible shortcomings
and improvements will be discussed below.

I strongly recommend to anyone interested to follow the link and read the paper
as most of the material does not require extensive expertise and concepts are
clearly explained.

## Introduction

One of the biggest roadblocks to training an artificial neural network (ANN)
is determining the proper topology of the network. If the size of the network
is too small, then it cannot solve the problem. On the other hand, if the size
of the network is too large, search for the solution becomes too slow as
the computational power required grows exponentially relative to the size
of the network.

Finding the right network structure for the job at hand is often part of the
most time consuming process in dealing with ANNs. Starting with a wrong network
structure, tuning of other hyperparameters, such as deciding learning rate,
batch optimization, weight initialization, etc., each of which is associated
with numerous variables to tune, becomes wasted labor.

In the field of machine learning (ML), whatever the problem at hand may be,
under the hood, the main goal is to automate the process of finding the right
variables. For example, at the lowest level, this is finding the right weight
matrices via gradient descent. At a higher level, we often see other examples
where a variety of adaptive algorithms are utilized. An algorithm that
searches for the right topology on its own could then be considered as
automation at the highest level, and could become an indispensable tool for ML
with ANNs.

## TWEANN and NEAT
