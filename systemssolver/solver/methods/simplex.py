from typing import Optional

from systemssolver.solver.methods.solvermethod import SolverMethod
from systemssolver.solver.problem import Problem
from systemssolver.solver.solution import Solution


class SimplexSolver(SolverMethod):

    def solve(self, problem: Problem) -> Optional[Solution]:
        if not self.can_solve(problem):
            return None



    def can_solve(self, problem: Problem) -> bool:
        return len(problem.objectives) == 1
