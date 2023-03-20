from illness import Illness
from simulation import Simulation


# TODO: define the relevant parameters here
class Covid(Illness):
    contagion_rate = 0.6
    resistance_to_vaccine = 0.25

    def __init__(self):
        super().__init__(self.contagion_rate, self.resistance_to_vaccine)


class Flu(Illness):
    contagion_rate = 0.2
    resistance_to_vaccine = 0.1

    def __init__(self):
        super().__init__(self.contagion_rate, self.resistance_to_vaccine)


if __name__ == "__main__":
    simulation = Simulation(
        population_size=1000,
        simulation_time=10000,
        n_initial_cases=5,
        vaccine_policy=20,
        quarantine_duration_vaccinated=7,
        quarantine_duration_not_vaccinated=12,
        number_days_until_quarantine=2,
        number_days_to_get_healthy_vaccinated=10,
        number_days_to_get_healthy_not_vaccinated=14,
        number_days_immunity=14,
        immunity_factor_per_time=2,  # Do not change!
        contagion_distance=2,
        max_position=25,
        illness=Covid(),
        vaccination_rate=0.1,
        vaccine_efficiency=0.8,
        incubation_time=2
    )

    simulation.simulate()
