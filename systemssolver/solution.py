from typing import Set

from systemssolver.modeling.variables import Variable


class Solution:
    def __init__(self, variables: Set[Variable]):
        self.variables = variables

    def __str__(self):
        return ', '.join('{}={}'.format(var.name, var.val) for var in self.variables)
