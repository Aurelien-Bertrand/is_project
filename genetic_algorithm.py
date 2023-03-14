import random
from typing import Any

import numpy as np


class Problem:
    population_size: int
    fitness: Any
    population_generation: Any
    mutation: Any

    def __init__(self, size: int, f: Any, p: Any, m: Any):
        self.population_size = size
        self.fitness = f
        self.population_generation = p
        self.mutation = m

    def initialize_population(self) -> list:
        return self.population_generation(self.population_size)

    def compute_fitness(self, population) -> list:
        return self.fitness(population)

    def mutate(self, population, mutation_probability):
        return self.mutation(population, mutation_probability)


class GA:
    problem: Problem
    crossover_probability: float
    mutation_probability: float
    population: list
    mating_pool: list
    fitness: list

    def __init__(self, problem: Problem, pc: float, pm: float) -> None:
        self.problem = problem
        self.crossover_probability = pc
        self.mutation_probability = pm

    def run(self, number_of_generations: int):
        self._initialize_population()
        for i in range(number_of_generations):
            self._generate_new_population()
            self._show_information()

    def _initialize_population(self) -> None:
        self.population = self.problem.initialize_population()

    def _generate_new_population(self) -> None:
        self._selection()
        self._crossover()
        self.population = self.problem.mutate(self.population, self.mutation_probability)

    def _selection(self) -> None:
        self.fitness = self.problem.compute_fitness(self.population)

        elite_size = int(self.problem.population_size * 0.3)
        elite_indices = np.argsort(self.fitness)[-elite_size:]
        non_elite_indices = [i for i in range(len(self.fitness)) if i not in elite_indices]
        non_elite_fitness = [self.fitness[i] for i in non_elite_indices]
        total_fitness = sum(non_elite_fitness)

        selection_probabilities = [f / total_fitness for f in non_elite_fitness]
        elite_population = [self.population[i] for i in elite_indices]

        self.mating_pool = elite_population
        self.mating_pool += [
            self.population[np.random.choice(non_elite_indices, p=selection_probabilities)]
            for _ in range(len(self.population) - elite_size)
        ]

    def _crossover(self) -> None:
        temp_pop = []
        while len(self.mating_pool) > 0:
            p1 = self.mating_pool.pop(random.randrange(len(self.mating_pool)))
            p2 = self.mating_pool.pop(random.randrange(len(self.mating_pool)))
            x = random.random()
            if x <= self.crossover_probability:
                cut = random.randint(0, len(p1))
                temp_pop.append(p1[:cut] + p2[cut:])
                temp_pop.append(p2[:cut] + p1[cut:])
            else:
                temp_pop.append(p1)
                temp_pop.append(p2)

        self.population = temp_pop

    def _show_information(self) -> None:
        index_best_individual = sorted(
            range(len(self.population)),
            reverse=True,
            key=lambda i: self.fitness[i]
        )[0]
        best_individual = self.population[index_best_individual]
        best_individual_fitness = self.fitness[index_best_individual]
        print(f"Best individual in population {best_individual}: \nIndividual's fitness: {best_individual_fitness}\r")