from typing import Set

from systemssolver.modeling.variables import Variable


class Solution:
    def __init__(self, variables: Set[Variable]):
        self.variables = variables

    def __str__(self):
        return ', '.join('{}={}'.format(var.name, var.val) for var in self.variables)

    def __neg__(self):
        for var in self.variables:
            var.val = -var.val
        return self

    def __eq__(self, other):
        if not isinstance(other, Solution):
            return False

        name_vals = {var.name: var.val for var in self.variables}
        other_name_vals = {var.name: var.val for var in other.variables}
        return name_vals == other_name_vals
