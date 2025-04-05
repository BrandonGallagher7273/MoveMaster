MoveMaster 
----------
## Overview
MoveMaster was established with the goal of leveraging physics and machine learning to identify the most optimal move set for winning popular online and tabletop games. Depending on which game is selected, MoveMaster allows the user to specify various parameters that influence gameplay. In Jenga, for instance, a user can specify the current state of the game (i.e., whether the game is just starting, or the game is currently in progress, and the displacement of blocks). After all parameters are set, the software will produce the best possible move that a player could make.\
Considering the computational complexity associated with machine learning and physics simulation, MoveMaster is developed as a desktop application. C# serves as our primary language for physics simulation, as it allows us to make use of Unity’s proprietary physics engine. In addition to C#, Python offers a number of libraries and frameworks that simplify the implementation of machine learning models.
## Goals
During U24, we developed a game-state simulator that algorithmically evaluates whether or not the current game state is a fail state (i.e., when gravity is applied, whether or not the tower would fall over). Our next step is developing and training an artificial intelligence model to calculate the next move with the highest probability of success. Since training this model will require supervised learning techniques, we anticipate spending quite some time on this step in particular.
## Milestones
### Beginning of Semester
* Finish the simulation– add ability to add blocks to the top of the tower once removed. 
* Add the ability to simulate a game based on an inputted sequence of events. 
* Create a CPU with varying difficulties that a user can play against.
### Mid-semester
* Generate thousands of games worth of training data that our Machine Learning algorithm will use.
* Develop the Machine Learning algorithm that will learn the game of Jenga to tell the player the best possible move to increase likelihood of a win.
* Test our model thoroughly and make edits as needed.
### End of semester
* Ensure our repository is up to date, including updated code and readme
* Create an outline document for next steps post-semester
