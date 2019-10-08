from project1.solver.problem import Problem
from project1.solver.solution import Solution
from project1.solver.solver import Solver


class SimplexSolver(Solver):

    def solve(self, problem: Problem) -> Solution:
        pass

    def can_solve(self, problem: Problem) -> bool:
        return problem.num_objectives == 1
