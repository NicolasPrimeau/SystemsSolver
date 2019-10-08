from typing import List

from systemssolver.modeling.equation import Constraint
from systemssolver.modeling.objective import Objective


class Problem:

    def __init__(self):
        self._objective_functions: List[Objective] = list()
        self._constraints: List[Constraint] = list()

    def add_objective(self, obj: Objective):
        self._objective_functions.append(obj)

    def add_constraint(self, obj: Constraint):
        self._constraints.append(obj)

    @property
    def objectives(self) -> List[Objective]:
        return self._objective_functions

    @property
    def constraints(self) -> List[Constraint]:
        return self._constraints
