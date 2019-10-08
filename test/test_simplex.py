import unittest

from systemssolver.methods.simplex import SimplexSolver
from systemssolver.modeling.equation import Expression, Constraint, EqualitySigns
from systemssolver.modeling.objective import Objective, ObjectiveGoal
from systemssolver.modeling.variables import Term, Variable, Constant
from systemssolver.problem import Problem


class SimplexTest(unittest.TestCase):

    def test_simplex_standard_form(self):
        problem = Problem()
        problem.add_objective(Objective(expression=Expression(terms=[
            Term(coef=8, var=Variable(name="x1")),
            Term(coef=10, var=Variable(name="x2")),
            Term(coef=7, var=Variable(name="x3"))
        ]), goal=ObjectiveGoal.MAXIMIZE))

        problem.add_constraint(Constraint(left=Expression(terms=[
            Term(coef=1, var=Variable(name="x1")),
            Term(coef=3, var=Variable(name="x2")),
            Term(coef=2, var=Variable(name="x3"))
        ]), right=Expression(terms=[Term(var=Constant(name="c1", val=10))]), sign=EqualitySigns.LE))

        problem.add_constraint(Constraint(left=Expression(terms=[
            Term(coef=1, var=Variable(name="x1")),
            Term(coef=5, var=Variable(name="x2")),
            Term(coef=1, var=Variable(name="x3"))
        ]), right=Expression(terms=[Term(var=Constant(name="c2", val=8))]), sign=EqualitySigns.LE))

        solver = SimplexSolver()
        solution = solver.solve(problem)

        expected_vals = {'x1': 8, 'x2': 0, 'x3': 0, 's0': 2, 's1': 0, 'z': 64}
        for var in solution.variables:
            print(var.name)
            print(var.val)
            
        for var in solution.variables:
            self.assertEqual(expected_vals.get(var.name), var.val)
