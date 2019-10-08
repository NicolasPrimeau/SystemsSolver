from typing import List

from project1.solver.modeling.inequality import Inequality
from project1.solver.modeling.objective import ObjectiveFunction


class Problem:

    def __init__(self):
        self._objective_functions: List[ObjectiveFunction] = list()
        self._constraints: List[Inequality] = list()

    def append_objective_function(self, obj: ObjectiveFunction):
        self._objective_functions.append(obj)

    @property
    def num_objectives(self) -> int:
        return len(self._objective_functions)

    def append_constraints(self, obj: Inequality):
        self._constraints.append(obj)

    @property
    def num_constraints(self) -> int:
        return len(self._constraints)
