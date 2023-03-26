# Intelligent Systems Assignment

This assignment aims at implementing a simulation of a virus' propagation with multiple parameters to make it as close to reality as possible. Then, using a genetic algorithm (GA), optimal parameters are optimized to hinder the progression of the virus as much as possible within a population. In this case, the flu and covid-19 viruses are considered and tested. 

In order to make the simulation realistic, the following procedure has been implemented: 
1. People infect each other if they are sufficiently close to each other, with a certain probability.
2. People are placed in quarantine after a certain amount of days, if possitive. 
3. People move around in a given place, if not in quarantine.
4. People get vaccinated upon a certain probability.

The GA implemented is used to optimize a set of 4 parameters in order to prevent the deseases from spreading too much:
- The number of people initially vaccinated at the start of the simulation;
- The number of days spent in quarantine when vaccinated;
- The number of days spent in quarantine when not vaccinated;
- The number of days before being placed in quarantine, if possitive.

Note that the infections depend on several parameters: odds, vaccine effet and immunity effect to make it as realistic as possible.
