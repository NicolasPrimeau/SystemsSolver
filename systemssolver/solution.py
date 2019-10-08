from typing import Set

from systemssolver.modeling.variables import Variable


class Solution:
    def __init__(self, variables: Set[Variable]):
        self.variables = variables
