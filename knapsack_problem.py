import random

from genetic_algorithm import Problem, GA

# TODO: delete this file in the end

def _compute_total_weight(individual: list) -> int:
    return sum([item[1] * item[2] for item in individual])


def fitness(population: list) -> list:
    fitness = []
    for ind in population:
        if _compute_total_weight(individual=ind) > 100:
            fitness.append(0)
        else:
            fitness.append(sum([item[0] * item[2] for item in ind]))

    return fitness


def mutate(population: list, prob: float) -> list:
    new_population = []
    for ind in population:
        new_individual = []
        for item in ind:
            x = random.random()
            if x <= prob:
                item[2] = abs(item[2] - 1)
            new_individual.append(item)

        new_population.append(new_individual)

    return new_population


def generate_population(size: int) -> list:
    n_items = 20
    weights = [random.randint(1, 10) for j in range(n_items)]
    population = []
    for i in range(size):
        individual = []
        for j in range(n_items):
            individual.append([j+1, weights[j], random.randint(0, 1)])

        population.append(individual)

    return population


if __name__ == "__main__":
   problem = Problem(size=500, f=fitness, p=generate_population, m=mutate)
   ga = GA(problem=problem, pc=0.9, pm=0.01)
   ga.run(1000)
