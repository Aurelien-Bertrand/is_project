from copy import deepcopy
from typing import List

import numpy as np


class Person:
    _id: int
    _is_ill: bool
    _is_vaccinated: bool
    _days_in_quarantine: int
    _position: List[int]
    _initial_position: List[int]
    _time_last_contamination: int
    _has_been_infected: bool

    def __init__(self, id: int, is_ill: bool, is_vaccinated: bool, max_position: int) -> None:
        self._id = id
        self._is_ill = is_ill
        self._is_vaccinated = is_vaccinated
        self._days_in_quarantine = 0
        self._initial_position = [np.random.randint(max_position), np.random.randint(max_position)]
        self._position = deepcopy(self._initial_position)
        self._time_last_contamination = 0
        self._has_been_infected = True if is_ill else False

    def move(self, max_position: int) -> None:
        # Put person back to his house if in quarantine
        if self.is_in_quarantine():
            self._position = self._initial_position
            return

        old_pos = self.get_position()
        for i in range(len(old_pos)):
            increment = np.random.choice([-1, 0, 1])
            if old_pos[i] + increment > max_position:
                self._position[i] = 0
            elif old_pos[i] + increment < 0:
                self._position[i] = max_position
            else:
                self._position[i] += increment

        # print(f"Person {self._id} moved from {old_pos} to {self._position}")

    def update_quarantine(
        self,
        time: int,
        quarantine_duration_vaccinated: int,
        quarantine_duration_not_vaccinated: int,
        number_days_until_quarantine: int,
        number_days_to_get_healthy_vaccinated: int,
        number_days_to_get_healthy_not_vaccinated: int
    ) -> None:
        if not self.is_ill():
            self._days_in_quarantine = 0
            self._is_ill = False
            return

        if self.is_vaccinated():
            # Get healthy again
            if time - self._time_last_contamination >= number_days_to_get_healthy_vaccinated and self._has_been_infected:
                # print(f"Person {self._id} is healthy again")
                self._days_in_quarantine = 0
                self._is_ill = False
                return
            # If quarantined finish, get out
            if self._days_in_quarantine >= quarantine_duration_vaccinated:
                # print(f"Person {self._id} is leaving quarantine")
                self._days_in_quarantine = 0
                return
        else:
            # Get healthy again
            if time - self._time_last_contamination >= number_days_to_get_healthy_not_vaccinated:
                # print(f"Person {self._id} is healthy again")
                self._days_in_quarantine = 0
                self._is_ill = False
                return
            # If quarantined finish, get out
            if self._days_in_quarantine >= quarantine_duration_not_vaccinated:
                # print(f"Person {self._id} is leaving quarantine")
                self._days_in_quarantine = 0
                return

        # Put in quarantine
        if time - self._time_last_contamination >= number_days_until_quarantine:
            self._days_in_quarantine += 1
            # print(
            #     f"Person {self._id} is entering quarantine" if self._days_in_quarantine == 1
            #     else f"Person {self._id} is in quarantine since {self._days_in_quarantine} days"
            # )

    def becomes_ill(self, time: int, id_infector: int, number_days_immunity: int) -> None:
        # If the person is already infected, do nothing
        if self.is_ill():
            return

        # If the person has been infected already, they may have an immunity
        if time - self._time_last_contamination <= number_days_immunity and self._has_been_infected:
            return

        # print(f"Person {self._id} is infected by Person {id_infector}")
        self._is_ill = True
        self._time_last_contamination = time
        self._has_been_infected = True

    def get_position(self) -> List[int]:
        return self._position.copy()

    def get_vaccinated(self) -> None:
        # print(f"Person {self._id} gets vaccinated")
        self._is_vaccinated = True

    def is_ill(self) -> bool:
        return bool(self._is_ill)

    def is_vaccinated(self) -> bool:
        return bool(self._is_vaccinated)

    def is_in_quarantine(self) -> bool:
        return bool(self._days_in_quarantine)

    def get_id(self) -> int:
        return self._id

    def get_last_infection_time(self) -> int:
        return self._time_last_contamination

    def has_been_infected(self) -> bool:
        return self._has_been_infected
