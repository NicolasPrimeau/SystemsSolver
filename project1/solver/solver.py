from abc import ABC, abstractmethod

from project1.solver.problem import Problem
from project1.solver.solution import Solution


class Solver(ABC):

    @abstractmethod
    def can_solve(self, problem: Problem) -> bool:
        pass

    @abstractmethod
    def solve(self, problem: Problem) -> Solution:
        pass
