from typing import List

import numpy as np

from illness import Illness
from person import Person


def _compute_Manhattan_distance(pos1: List[int], pos2: List[int]):
    return abs(pos1[0] - pos2[0]) + abs(pos1[0] - pos2[0])


class Simulation:
    population: List[Person]

    simulation_time: int
    quarantine_duration_vaccinated: int
    quarantine_duration_not_vaccinated: int
    number_days_until_quarantine: int
    number_days_to_get_healthy_vaccinated: int
    number_days_to_get_healthy_not_vaccinated: int
    number_days_immunity: int
    immunity_factor_per_time: float
    contagion_distance: int
    max_position: int
    illness: Illness
    vaccination_rate: float
    vaccine_efficiency: float
    incubation_time: int

    def __init__(
            self,
            population_size: int,
            simulation_time: int,
            n_initial_cases: int,
            vaccine_policy: int,  # To be optimized (should not exceed something)
            quarantine_duration_vaccinated: int,  # To be optimized (should not exceed something)
            quarantine_duration_not_vaccinated: int,  # To be optimized (should not exceed something)
            number_days_until_quarantine: int,  # To be optimized (should not exceed something)
            number_days_to_get_healthy_vaccinated: int,
            number_days_to_get_healthy_not_vaccinated: int,
            number_days_immunity: int,
            immunity_factor_per_time: int,
            contagion_distance: int,
            max_position: int,
            illness: Illness,
            vaccination_rate: float,
            vaccine_efficiency: float,
            incubation_time: int,
            seed=100,
    ) -> None:
        self.simulation_time = simulation_time
        self.quarantine_duration_vaccinated = quarantine_duration_vaccinated
        self.quarantine_duration_not_vaccinated = quarantine_duration_not_vaccinated
        self.number_days_until_quarantine = number_days_until_quarantine
        self.number_days_to_get_healthy_vaccinated = number_days_to_get_healthy_vaccinated
        self.number_days_to_get_healthy_not_vaccinated = number_days_to_get_healthy_not_vaccinated
        self.number_days_immunity = number_days_immunity
        self.immunity_factor_per_time = immunity_factor_per_time
        self.contagion_distance = contagion_distance
        self.max_position = max_position
        self.illness = illness
        self.vaccination_rate = vaccination_rate
        self.vaccine_efficiency = vaccine_efficiency
        self.incubation_time = incubation_time

        self._generate_initial_population(
            population_size=population_size, n_initial_cases=n_initial_cases, vaccine_policy=vaccine_policy, seed=seed
        )

    def _generate_initial_population(self, population_size: int, n_initial_cases: int, vaccine_policy: int, seed: int):
        assert n_initial_cases <= population_size

        rng = np.random.RandomState(seed)

        illness = np.zeros(population_size)
        illness[:n_initial_cases] = 1
        rng.shuffle(illness)
        illness = list(map(bool, illness))

        vaccines = np.zeros(population_size)
        vaccines[:vaccine_policy] = 1
        rng.shuffle(vaccines)
        vaccines = list(map(bool, vaccines))

        self.population = [
            Person(id=i, is_ill=illness[i], is_vaccinated=vaccines[i], max_position=self.max_position)
            for i in range(population_size)
        ]

    def _infections(self, time: int) -> None:
        infected = [index for index, individual in enumerate(self.population) if
                    individual.is_ill() and not individual.is_in_quarantine()]
        infectible = [index for index, individual in enumerate(self.population) if
                      not individual.is_ill() and not individual.is_in_quarantine()]

        for i in infected:
            for j in infectible:
                pos1, pos2 = self.population[i].get_position(), self.population[j].get_position()
                if _compute_Manhattan_distance(pos1=pos1, pos2=pos2) <= self.contagion_distance:
                    self._infect_each_other(time=time, person1=self.population[i], person2=self.population[j])

    def _infect_each_other(self, time: int, person1: Person, person2: Person) -> None:
        person_infecting = person1 if person1.is_ill() else person2
        person_infected = person1 if person2.is_ill() else person2
        # Effect that the vaccine has on likelihood to get infected
        vaccine_effect = person_infected.is_vaccinated() * (
                self.illness.resistance_to_vaccine - self.vaccine_efficiency)
        # Effect that immunity due to already being infected has on likelihood to get infected
        immunity_effect = 0 if person_infected.get_last_infection_time() == 0 \
            else 1 / np.power(
            self.immunity_factor_per_time,
            (time - person_infected.get_last_infection_time()) * person_infected.has_been_infected()
        )
        # Infect each other based on likelihoods (vaccine reduces it, resistance increases it, immunity reduces it)
        if np.random.random() < self.illness.contagion_rate + vaccine_effect - immunity_effect:
            # Incubation time
            if time - person_infecting.get_last_infection_time() > self.incubation_time:
                person_infected.becomes_ill(
                    time=time, id_infector=person_infecting.get_id(), number_days_immunity=self.number_days_immunity
                )

    def _update_quarantines(self, time: int) -> None:
        [
            x.update_quarantine(
                time=time,
                quarantine_duration_vaccinated=self.quarantine_duration_vaccinated,
                quarantine_duration_not_vaccinated=self.quarantine_duration_not_vaccinated,
                number_days_until_quarantine=self.number_days_until_quarantine,
                number_days_to_get_healthy_vaccinated=self.number_days_to_get_healthy_vaccinated,
                number_days_to_get_healthy_not_vaccinated=self.number_days_to_get_healthy_not_vaccinated
            ) for x in self.population
        ]

    def _move(self) -> None:
        [x.move(max_position=self.max_position) for x in self.population]

    def _vaccination(self) -> None:
        # People get possibly vaccinated
        for x in self.population:
            if np.random.random() < self.vaccination_rate:
                x.get_vaccinated()

    def _compute_number_cases(self) -> int:
        return sum([1 if x.is_ill() else 0 for x in self.population])

    def _compute_new_cases(self, time: int) -> int:
        return sum([1 if (x.is_ill() and x.get_last_infection_time() == time) else 0 for x in self.population])

    # Returns the number of cases at the end of the simulation
    def simulate(self) -> (int, int):
        cumulated_cases = 0
        new_cases = 0
        for tick in range(0, self.simulation_time):
            self._infections(time=tick)
            self._update_quarantines(time=tick)
            self._move()
            self._vaccination()

            new_cases = self._compute_new_cases(tick)
            cumulated_cases += new_cases

            if self._compute_number_cases() == 0:
                break

        return new_cases, cumulated_cases
