from typing import Optional

from systemssolver.methods.solvermethod import SolverMethod
from systemssolver.modeling.equation import EqualitySigns, convert_constraint_to, Constraint
from systemssolver.modeling.objective import ObjectiveGoal, convert_objective_to_goal
from systemssolver.modeling.variables import Variable
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
        slacked_constrains = [
            Constraint(left=constraint.left + slack, right=constraint.right, sign=EqualitySigns.EQUAL)
            for constraint, slack in zip(lte_constraints, slack_variables)
        ]

        # Creating the tableau

        # Pivot variables

        # Creating a new tableau

        # Checking for optimality
        
        # Identify optimal values

    def can_solve(self, problem: Problem) -> bool:
        return len(problem.objectives) == 1
