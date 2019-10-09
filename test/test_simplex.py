import unittest

from systemssolver.methods.simplex import SimplexSolver
from systemssolver.modeling.equation import Expression, Constraint, EqualitySigns
from systemssolver.modeling.objective import Objective, ObjectiveGoal
from systemssolver.modeling.variables import Term, Variable, Constant
from systemssolver.problem import Problem
from systemssolver.tracing.hook import PrintSolutionHook


class SimplexTest(unittest.TestCase):

    def test_simplex_standard_form(self):
        x1 = Variable(name="x1")
        x2 = Variable(name="x2")
        x3 = Variable(name="x3")
        problem = Problem()
        problem.add_objective(Objective(
            expression=Expression(terms=[Term(coef=8, var=x1), Term(coef=10, var=x2), Term(coef=7, var=x3)]),
            goal=ObjectiveGoal.MAXIMIZE
        ))

        problem.add_constraint(Constraint(
            left=Expression(terms=[Term(coef=1, var=x1), Term(coef=3, var=x2), Term(coef=2, var=x3)]),
            right=Expression(terms=[Term(var=Constant(name="c1", val=10))]),
            sign=EqualitySigns.LE
        ))

        problem.add_constraint(Constraint(
            left=Expression(terms=[Term(coef=1, var=x1), Term(coef=5, var=x2), Term(coef=1, var=x3)]),
            right=Expression(terms=[Term(var=Constant(name="c2", val=8))]),
            sign=EqualitySigns.LE
        ))

        solver = SimplexSolver()
        solution = solver.solve(problem, tracing_hook=PrintSolutionHook())

        expected_vals = {x1.name: 8, x2.name: 0, x3.name: 0, 's0': 2, 's1': 0, 'z': 64}

        for var in solution.variables:
            self.assertEqual(expected_vals.get(var.name), var.val)

    def test_simplex_project1(self):
        x = Variable(name="x")
        y = Variable(name="y", inverted=True)

        problem = Problem()
        problem.add_objective(Objective(
            expression=Expression(terms=[Term(coef=1, var=x), Term(coef=1.2, var=y)]),
            goal=ObjectiveGoal.MAXIMIZE
        ))

        problem.add_constraint(Constraint(
            left=Expression(terms=[Term(coef=2, var=x), Term(coef=1, var=y)]),
            right=Expression(terms=[Term(var=Constant(name="c0", val=sum([6, 3, 5, 2, 1, 4, 5])))]),
            sign=EqualitySigns.LE
        ))

        problem.add_constraint(Constraint(
            left=Expression(terms=[Term(coef=1, var=x), Term(coef=3, var=y)]),
            right=Expression(terms=[Term(var=Constant(name="c1", val=120))]),
            sign=EqualitySigns.LE)
        )

        solver = SimplexSolver()
        solution = solver.solve(problem, tracing_hook=PrintSolutionHook())

        expected_vals = {x.name: 8, y.name: 0, 's0': 2, 's1': 0, 'z': 64}
        print(str(solution))

        for var in solution.variables:
            self.assertEqual(expected_vals.get(var.name), var.val)
