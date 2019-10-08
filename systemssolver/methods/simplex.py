from typing import Optional

from systemssolver.methods.solvermethod import SolverMethod
from systemssolver.problem import Problem
from systemssolver.solution import Solution
from systemssolver.tracing.hook import TracingHook


class Tableau:

    def __init__(self):
        pass


class SimplexSolver(SolverMethod):

    def solve(self, problem: Problem, tracing_hook: TracingHook = None) -> Optional[Solution]:
        if not self.can_solve(problem):
            return None

        # Standard form,
        # (1) must be a maximization problem,
        # (2) all linear constraints must be in a less-than-or-equal-to inequality,
        # (3) all variables are non-negative.
        # Introducing slack variables: additional variables that make inequalities to
        # equal. The new system is called canonical form.
        # Creating the tableau
        # Pivot variables
        # Creating a new tableau
        # Checking for optimality
        # Identify optimal values

    def can_solve(self, problem: Problem) -> bool:
        return len(problem.objectives) == 1
