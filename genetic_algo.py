import random

import numpy as np

from main import Covid
from simulation import Simulation
from random import Random


def simulate(individual):
    simulation = Simulation(
        population_size=200,
        simulation_time=100,
        n_initial_cases=5,
        vaccine_policy=individual[0],
        quarantine_duration_vaccinated=individual[1],
        quarantine_duration_not_vaccinated=individual[2],
        number_days_until_quarantine=individual[3],
        number_days_to_get_healthy_vaccinated=10,
        number_days_to_get_healthy_not_vaccinated=14,
        number_days_immunity=7,
        immunity_factor_per_time=2,  # Do not change!
        contagion_distance=10,
        max_position=25,
        illness=Covid(),
        vaccination_rate=0.05,
        vaccine_efficiency=0.6,
        incubation_time=2
    )

    return simulation.simulate()


def _generatePop():
    individuals = []
    for _ in range(pop_size):
        individual = [Random().randint(0, j) for j in max_values]
        individuals.append(individual)

    return individuals


def _compute_fitness(individual: list):
    fitness = sum(simulate(individual))
    penalty = 0
    for i in range(len(individual)):
        if individual[i] > max_values[i]:
            penalty += 1000

    return 5 / (fitness + penalty)


def _generate_fittest(population: list, fitness: list):
    tournament_indices = random.sample(range(len(population)), tournament_size)
    tournament = [population[i] for i in tournament_indices]

    fitness = [fitness[fit] for fit in tournament_indices]
    max_index = fitness.index(max(fitness))
    fitness[max_index] = -1

    return tournament[max_index]


def _generate_offspring(p1, p2):
    if Random().random() < crossover_prob:
        point = Random().randint(1, len(p1) - 1)
        c1 = p1[:point] + p2[point:]
        c2 = p2[:point] + p1[point:]
    else:
        c1 = p1
        c2 = p2

    for i in range(len(p1)):
        for c in [c1, c2]:
            if Random().random() < mutation_prob:
                c[i] = Random().randint(0, max_values[i])

    return c1, c2


if __name__ == '__main__':
    max_values = [20,14,14,7]
    pop_size = 50
    tournament_size = int(pop_size / 2)

    crossover_prob = 0.9
    mutation_prob = 0.01

    pop = _generatePop()

    for i in range(100):
        pop_mat = []
        fitness_scores = [_compute_fitness(individual) for individual in pop]
        while len(pop_mat) != len(pop):
            ind = _generate_fittest(population=pop, fitness=fitness_scores)
            pop_mat.append(ind)

        pop = []
        while len(pop_mat) != 0:
            parent1 = Random().choice(pop_mat)
            pop_mat.remove(parent1)

            parent2 = Random().choice(pop_mat)
            pop_mat.remove(parent2)

            child1, child2 = _generate_offspring(parent1, parent2)

            pop.append(child1)
            pop.append(child2)

        index_best_individual = np.argmax(fitness_scores)
        best_individual = pop[index_best_individual]
        best_individual_score = fitness_scores[index_best_individual]
        print(f"Gen {i}: best score ", best_individual_score, best_individual)

        if best_individual_score == 1:
            break
