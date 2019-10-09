from abc import ABC, abstractmethod

from systemssolver.problem import Problem
from systemssolver.solution import Solution
from systemssolver.tracing.hook import TracingHook


class SolverMethod(ABC):

    @abstractmethod
    def can_solve(self, problem: Problem) -> bool:
        pass

    @abstractmethod
    def solve(self, problem: Problem, tracer_hook: TracingHook = None) -> Solution:
        pass

