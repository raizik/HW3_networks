# Switch Simulator
```switch.py``` is an event-driven simulation of a switch with multiple input and output ports. The routing rules are set by an NXM probabilities matrix setting P[i,j] to be the probability to route a frame arriving to input port i to output port j. 
## Simulator input
* T - the total simulation time. After T time units, there'll be no more frames arriving at the switch's input ports and the already existing frames would be handled.
* N - number of input ports
* M - number of output ports
* P[i,j] - the probabilities matrix
* lambda[i] - the arrival rates on the ith input port
* Q[i] - the ith output port's queue size
* mu[i] - the service rate of ith output port
## Run example
```simulator 1000 1 2 0.1 0.9 200 2 10 20 180```

In this case the simulation would run for 1000 time units with a single input port and two output ports. The probability for routing a frame to the first output port is 0.1 and the probability for routing to the second is 0.9. The frames' arrival rate is 200 frames in a unit of time, the transmission rate on the first output port is 20 and on the second is 180 frames per unit of time. The length of the first port's queue is 2 and of the second's 10.
