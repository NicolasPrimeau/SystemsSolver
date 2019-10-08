from systemssolver.solver.problem import Problem


class Solution:
    def __init__(self, problem: Problem):
        self._problem = problem
        self._vars = dict()

        for objective in problem.objectives:
            for term in objective.expression.terms:
                self._vars[term.var] = term.var.val

        for constraint in problem.constraints:
            for term in constraint.right.terms:
                self._vars[term.var] = term.var.val
            for term in constraint.left.terms:
                self._vars[term.var] = term.var.val

    def copy(self):
        solution = Solution(problem=self._problem)
        solution._vars.update(self._vars)
        return solution
