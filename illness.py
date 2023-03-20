class Illness:
    contagion_rate: float
    resistance_to_vaccine: float

    def __init__(self, contagion_rate: float, resistance_to_vaccine: float):
        self.contagion_rate = contagion_rate
        self.resistance_to_vaccine = resistance_to_vaccine
