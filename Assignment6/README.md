# Northwestern University Course - Artificial Life


## Assignment 6: generate random 1D creature morphologies

[video](https://youtu.be/ZTteUG4CstI)

### Step1. Run

  In this assignment, I create a program that generates a kinematic chain (a jointed, motorized, innervated, sensorized snake) with a: random number of randomly shaped links with random sensor placement along the chain. Links with and without sensors should be colored green and blue, respectively. Then I use EA(Evolutation Algorithm) to make robot crawl. The EA try to maximize the fitness function. The fitness of EA is `-Xposition`.

  Notice that this program needs at least 60 cpus to run. Because the `numberOfGenerations=3` and `populationSize=40`. To run the EA, use following command: 
  
  ```
  python search.py
  ```

### Step2. Replay

  To replay a single result in the video, run this:
  
  ```
  python replay.py best
  ```


  ![](./data/illustration.png) | ![](./data/combine4.gif)
  :-------------------------:|:-------------------------:

