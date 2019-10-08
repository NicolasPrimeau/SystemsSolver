from typing import Optional, List, Set

from systemssolver.methods.solvermethod import SolverMethod
from systemssolver.modeling.equation import EqualitySigns, convert_constraint_to, Constraint, Expression
from systemssolver.modeling.objective import ObjectiveGoal, convert_objective_to_goal
from systemssolver.modeling.variables import Variable
from systemssolver.problem import Problem
from systemssolver.solution import Solution
from systemssolver.tracing.hook import TracingHook


class Tableau:

    def __init__(self, objective: Expression, constraints: List[Constraint]):
        self._objective = objective
        self._constraints = constraints
        self._check_valid()
        self._tableau = self._build_tableau()

    def step(self) -> bool:
        # Pivot variables

        # Creating a new tableau

        # Checking for optimality

        # Identify optimal values
        pass

    def to_solution(self) -> Solution:
        pass

    def _check_valid(self):
        for term in self._objective.terms:
            if term.coef.val < 0:
                raise RuntimeError()

        for constraint in self._constraints:
            if constraint.sign != EqualitySigns.LE:
                raise RuntimeError
            for term in constraint.left.terms:
                if term.coef.val < 0:
                    raise RuntimeError()
            if len(constraint.right.terms) != 1:
                raise RuntimeError()

    def _build_tableau(self):
        self._var_order = list(sorted(self._get_variables(), key=lambda var: var.name))
        tableau = [[0 for _ in range(len(self._var_order) + 1)] or _ in range(len(self._constraints) + 1)]

        for row_idx, constraint in enumerate(self._constraints):
            for term in constraint.left.terms:
                var_idx = self._var_order.index(term.var)
                tableau[row_idx][var_idx] = term.coef.val
            tableau[row_idx][-1] = constraint.right.terms[0].var.val

        for term in self._objective.terms:
            var_idx = self._var_order.index(term.var)
            tableau[-1][var_idx] = term.coef.val
        return tableau

    def _get_variables(self) -> Set[Variable]:
        variables = set()

        for term in self._objective.terms:
            variables.add(term.var)

        for constraint in self._constraints:
            for term in constraint.left.terms:
                variables.add(term.var)

        obj_var = Variable(name="z")
        i = 0
        while obj_var in variables:
            obj_var = Variable(name="z{}".format(i))
            i += 1
        variables.add(obj_var)
        return variables


class SimplexSolver(SolverMethod):

    def solve(self, problem: Problem, tracing_hook: TracingHook = None) -> Optional[Solution]:
        if not self.can_solve(problem):
            return None

        objective = problem.objectives[0]

        # Standard form,
        # (1) must be a maximization problem,
        min_objective = convert_objective_to_goal(objective, ObjectiveGoal.MAXIMIZE)

        # (2) all linear constraints must be in a less-than-or-equal-to inequality,
        constraints = problem.constraints
        lte_constraints = [convert_constraint_to(constraint, EqualitySigns.LE) for constraint in constraints]

        # (3) all variables are non-negative.
        # TODO: not sure how to do this.

        # Introducing slack variables: additional variables that make inequalities to
        # equal. The new system is called canonical form.
        slack_variables = [Variable(name="s{}".format(i) for i in range(len(lte_constraints)))]
        slacked_constraints = [
            Constraint(left=constraint.left + slack, right=constraint.right, sign=EqualitySigns.EQUAL)
            for constraint, slack in zip(lte_constraints, slack_variables)
        ]

        # Creating the tableau
        tableau = Tableau(objective=min_objective.expression, constraints=slacked_constraints)
        while not tableau.step():
            if tracing_hook:
                solution = tableau.to_solution()
                if tracing_hook.step(solution):
                    return solution

        return tableau.to_solution()

    def can_solve(self, problem: Problem) -> bool:
        return len(problem.objectives) == 1
