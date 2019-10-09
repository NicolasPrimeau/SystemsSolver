import logging
from typing import Optional, List

from systemssolver.methods.solvermethod import SolverMethod
from systemssolver.modeling.equation import EqualitySigns, convert_constraint_to, Constraint, Expression
from systemssolver.modeling.objective import ObjectiveGoal, convert_objective_to_goal
from systemssolver.modeling.variables import Variable, Term
from systemssolver.problem import Problem
from systemssolver.solution import Solution
from systemssolver.tracing.hook import TracingHook


class Tableau:

    def __init__(self, objective: Expression, constraints: List[Constraint]):
        self._objective = objective
        self._constraints = constraints
        self._check_valid()
        self._variables = self._get_variables()
        self._tableau = self._build_tableau()

    def step(self) -> bool:
        if self._check_optimal():
            return True

        pivot_col = self._identify_pivot_col()
        pivot_row = self._identify_pivot_row(pivot_col)
        self._tableau = self._create_new_tableau(pivot_row, pivot_col)
        return self._check_optimal()

    def to_solution(self) -> Solution:
        optimal_variables = set()
        for var_idx, var in enumerate(self._variables):
            optimal_row_idx = None
            for row_idx, row in enumerate(self._tableau):
                if row[var_idx] == 1 and optimal_row_idx is None:
                    optimal_row_idx = row_idx
                elif row[var_idx] == 1 or row[var_idx] != 0:
                    optimal_row_idx = None
                    break

            if optimal_row_idx is None:
                var.val = 0
            else:
                var.val = self._tableau[optimal_row_idx][-1]
            optimal_variables.add(var)
        return Solution(optimal_variables)

    def _check_optimal(self) -> bool:
        return all(val >= 0 for val in self._tableau[-1][:-1])

    def _create_new_tableau(self, pivot_row, pivot_col):

        pivot_var_val = self._tableau[pivot_row][pivot_col]
        new_tableau = [list(x) for x in self._tableau]

        for col_idx, val in enumerate(self._tableau[pivot_row]):
            new_tableau[pivot_row][col_idx] /= pivot_var_val

        pivot_var_val = new_tableau[pivot_row][pivot_col]

        for row_idx, row in filter(lambda i_r: i_r[0] != pivot_row, enumerate(new_tableau)):
            row_multiplier = row[pivot_col] / pivot_var_val
            for col_idx, val in enumerate(row):
                new_tableau[row_idx][col_idx] -= row_multiplier * new_tableau[pivot_row][col_idx]
        return new_tableau

    def _identify_pivot_row(self, pivot_col) -> int:
        smallest_idx = None
        smallest_rh = None
        for idx, row in enumerate(self._tableau[:-1]):
            pivot_col_val = row[pivot_col]
            if pivot_col_val != 0:
                rh_indicator = row[-1] / pivot_col_val
                if smallest_idx is None or smallest_rh > rh_indicator > 0:
                    smallest_idx = idx
                    smallest_rh = rh_indicator
        return smallest_idx

    def _identify_pivot_col(self) -> int:
        return min(range(0, len(self._tableau[-1]) - 1), key=lambda idx: self._tableau[-1][idx])

    def _check_valid(self):
        if self._objective is None or len(self._constraints) == 0:
            logging.error("Need an objective and constraints ")
            raise RuntimeError()

        for constraint in self._constraints:
            if constraint.sign != EqualitySigns.EQUAL:
                logging.error(
                    "All constraints must be formulated as {} with a slack variable".format(EqualitySigns.EQUAL.value))
                raise RuntimeError()

            if len(constraint.right.terms) != 1:
                logging.error("All constraints must have a one constant on right hand side")
                raise RuntimeError()

    def _build_tableau(self):
        tableau = [[0 for _ in range(len(self._variables) + 1)] for _ in range(len(self._constraints) + 1)]

        for row_idx, constraint in enumerate(self._constraints):
            for term in constraint.left.terms:
                var_idx = self._variables.index(term.var)
                tableau[row_idx][var_idx] = term.coef
            tableau[row_idx][-1] = constraint.right.terms[0].coef

        for term in self._objective.terms:
            if term.var is not None:
                var_idx = self._variables.index(term.var)
                tableau[-1][var_idx] = -term.coef

        tableau[-1][self._variables.index(self._optimization_var)] = 1

        val = 0
        for term in self._objective.terms:
            if term.var is None:
                val += term.coef
        tableau[-1][-1] = val
        return tableau

    def _get_variables(self) -> List[Variable]:
        variables = set()

        for term in self._objective.terms:
            if term.var is not None:
                variables.add(term.var)

        for constraint in self._constraints:
            for term in constraint.left.terms:
                if term.var is not None:
                    variables.add(term.var)

        obj_var = Variable(name="z")
        i = 0
        while obj_var in variables:
            obj_var = Variable(name="z{}".format(i))
            i += 1
        self._optimization_var = obj_var
        variables.add(obj_var)
        return list(sorted(variables, key=lambda var: var.name))

    def __str__(self):
        x = ' '.join(map(str, self._variables)) + '\n'
        for row in self._tableau:
            x += str(row) + '\n'
        return x


class SimplexSolver(SolverMethod):

    def solve(self, problem: Problem, tracing_hook: TracingHook = None) -> Optional[Solution]:
        if not self.can_solve(problem):
            return None

        objective = problem.objectives[0]

        # Standard form,
        # (1) must be a maximization problem,
        min_objective = convert_objective_to_goal(objective, ObjectiveGoal.MAXIMIZE)

        # (2) all linear constraints must be in a less-than-or-equal-to inequality,
        lte_constraints = [convert_constraint_to(constraint, EqualitySigns.LE) for constraint in problem.constraints]
        for constraint in lte_constraints:
            lh_constants = [term for term in constraint.left.terms if term.var is None]
            rh_vars = [term for term in constraint.right.terms if term.var is not None]
            for term in lh_constants:
                constraint.left -= term
                constraint.right += term
            for var in rh_vars:
                constraint.left += var
                constraint.right -= var

        # (3) all variables are non-negative.

        # Introducing slack variables: additional variables that make inequalities to
        # equal. The new system is called canonical form.
        slack_variables = [Variable(name="s{}".format(i)) for i in range(len(lte_constraints))]
        slacked_constraints = [
            Constraint(left=constraint.left + Term(var=slack), right=constraint.right, sign=EqualitySigns.EQUAL)
            for constraint, slack in zip(lte_constraints, slack_variables)
        ]

        # Creating the tableau
        tableau = Tableau(objective=min_objective.expression, constraints=slacked_constraints)
        prev_solution = None
        last_solution = None
        while not tableau.step():
            solution = tableau.to_solution()
            if tracing_hook and not tracing_hook.step(solution):
                return solution
            if solution == prev_solution or solution == last_solution:
                logging.warning('Loop detected')
                return solution
            prev_solution = last_solution
            last_solution = solution
        return tableau.to_solution()

    def can_solve(self, problem: Problem) -> bool:
        return len(problem.objectives) == 1 and len(problem.constraints) > 0
