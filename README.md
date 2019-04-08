# Flappy Bird with NEAT

This project was inspired by
[this paper.](http://nn.cs.utexas.edu/downloads/papers/stanley.ec02.pdf)
This is my own take on neuroevolution borrowing many ideas presented in the
paper. This is just the first small project for implementing the idea from
scratch, and not everything is implemented to its full extent. Its possible
shortcomings and improvements will be discussed below.

Use `python game.py` to run the game normally, or `python game.py neat`
to run it with NEAT AI. Dependencies include `numpy` and `pygame` with
versions `1.16.2` and `1.9.4` used respectively when building the project.

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

## TWEANN, neuroevolution, and NEAT

Topology and weight evolving artificial neural network (TWEANN), as its name
suggests, is a type of ANN where it learns to decide what the optimal topology
for itself is on top of finding the right weights in the network.
In light of this new terminology, classical ANNs then could be considered as
weight evoloving aritificial neural network.

TWEANN is an encompassing term for any ANN evolving both its topology and
weights. Hence, there are many different kinds of TWEANN that can be found
in the literature. Now, neuroevolution is a type of TWEANN where an evolutionary
algorithm, or more commonly known as genetic algorithm (GA), is employed to
find the right ANN. In short, neuroevolution trains a batch of ANNs and then
creates a new generation of ANNs from the previous ones by breeding and mutating
ANNs.

How to go about evolving ANNs via GA then becomes the main focus of developing a
neuroevolution algorithm. Under such scheme, ANN is often referred to as
a genome. In any case, neuroevolution of augmented topologies (NEAT), cited
at the very beginning, is a proposed solution to this problem. Main ideas
of NEAT include genetic encoding (encoding the structure of ANN as a collection
of node genes and connection genes), historical markings (keeping track of
the history of genes), and protection of innovation through speciation
(protecting newly mutated genome).
