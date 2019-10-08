from abc import ABC, abstractmethod

from systemssolver.solver.problem import Problem
from systemssolver.solver.solution import Solution


class SolverMethod(ABC):

    @abstractmethod
    def can_solve(self, problem: Problem) -> bool:
        pass

    @abstractmethod
    def solve(self, problem: Problem) -> Solution:
        pass
