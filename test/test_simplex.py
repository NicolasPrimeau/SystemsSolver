import unittest

from systemssolver.methods.simplex import SimplexSolver
from systemssolver.modeling.equation import Expression, Constraint, EqualitySigns
from systemssolver.modeling.objective import Objective, ObjectiveGoal
from systemssolver.modeling.variables import Term, Variable
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
            right=Expression(terms=[Term(coef=10)]),
            sign=EqualitySigns.LE
        ))

        problem.add_constraint(Constraint(
            left=Expression(terms=[Term(coef=1, var=x1), Term(coef=5, var=x2), Term(coef=1, var=x3)]),
            right=Expression(terms=[Term(coef=8)]),
            sign=EqualitySigns.LE
        ))

        solver = SimplexSolver()
        solution = solver.solve(problem, tracing_hook=PrintSolutionHook())

        expected_vals = {x1.name: 8, x2.name: 0, x3.name: 0, 's0': 2, 's1': 0, 'z': 64}
        print(solution)
        for var in solution.variables:
            self.assertEqual(expected_vals.get(var.name), var.val)

    def test_assignment2(self):
        a = Variable(name="a")
        b = Variable(name="b")
        c = Variable(name="c")

        problem = Problem()
        problem.add_objective(Objective(
            expression=Expression(terms=[Term(coef=-5, var=a), Term(coef=-2, var=b), Term(coef=-30, var=c)]),
            goal=ObjectiveGoal.MINIMIZE
        ))

        problem.add_constraint(Constraint(
            left=Expression(terms=[Term(coef=1, var=a), Term(coef=9, var=b), Term(coef=12, var=c)]),
            right=Expression(terms=[Term(coef=180)]),
            sign=EqualitySigns.LE
        ))

        problem.add_constraint(Constraint(
            left=Expression(terms=[Term(coef=2, var=a), Term(coef=9, var=b), Term(coef=6, var=c)]),
            right=Expression(terms=[Term(coef=210)]),
            sign=EqualitySigns.LE
        ))
        solver = SimplexSolver()
        solution = solver.solve(problem, tracing_hook=PrintSolutionHook())
        expected_vals = {a.name: 80, b.name: 0, c.name: 8.33333, 's0': 0, 's1': 0, 'z': 650}
        print(solution)
        for var in solution.variables:
            self.assertAlmostEqual(expected_vals.get(var.name), var.val, 5)

    def test_unstandard_form(self):
        x = Variable(name="x")
        y = Variable(name="y")
        problem = Problem()
        problem.add_objective(Objective(
            expression=Expression(terms=[Term(coef=1, var=x), Term(coef=1.2, var=y), Term(coef=5)]),
            goal=ObjectiveGoal.MAXIMIZE
        ))

        problem.add_constraint(Constraint(
            left=Expression(terms=[Term(coef=2, var=x), Term(coef=1, var=y), Term(coef=1)]),
            right=Expression(terms=[Term(coef=sum([6, 3, 5, 2, 1, 4, 5]))]),
            sign=EqualitySigns.GE
        ))

        problem.add_constraint(Constraint(
            left=Expression(terms=[Term(coef=1, var=x), Term(coef=3, var=y)]),
            right=Expression(terms=[Term(coef=120)]),
            sign=EqualitySigns.LE)
        )
        solver = SimplexSolver()
        solution = solver.solve(problem, tracing_hook=PrintSolutionHook())

        expected_vals = {x.name: 0, y.name: 0, 's0': -27, 's1': 120, 'z': 5.0}
        print(solution)
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
            right=Expression(terms=[Term(coef=sum([6, 3, 5, 2, 1, 4, 5]))]),
            sign=EqualitySigns.LE
        ))

        problem.add_constraint(Constraint(
            left=Expression(terms=[Term(coef=1, var=x), Term(coef=3, var=y)]),
            right=Expression(terms=[Term(coef=120)]),
            sign=EqualitySigns.LE)
        )

        solver = SimplexSolver()
        solution = solver.solve(problem, tracing_hook=PrintSolutionHook())

        expected_vals = {x.name: 0, y.name: -26, 's0': 0, 's1': 42, 'z': 31.2}
        print(solution)
        for var in solution.variables:
            self.assertEqual(expected_vals.get(var.name), var.val)

    def test_question_2(self):
        a = Variable(name="a")
        b = Variable(name="b")

        problem = Problem()
        problem.add_objective(Objective(
            expression=Expression(terms=[Term(coef=5, var=a), Term(coef=8, var=b)]),
            goal=ObjectiveGoal.MAXIMIZE
        ))

        problem.add_constraint(Constraint(
            left=Expression(terms=[Term(coef=10, var=a), Term(coef=7, var=b)]),
            right=Expression(terms=[Term(coef=57)]),
            sign=EqualitySigns.LE
        ))

        problem.add_constraint(Constraint(
            left=Expression(terms=[Term(coef=5, var=a), Term(coef=9, var=b)]),
            right=Expression(terms=[Term(coef=46)]),
            sign=EqualitySigns.LE
        ))
        solver = SimplexSolver()
        solution = solver.solve(problem, tracing_hook=PrintSolutionHook())
        expected_vals = {a.name: 3.472727, b.name: 3.1818181, 's0': 0, 's1': 0, 'z': 42.81818181}
        print(solution)
        for var in solution.variables:
            self.assertAlmostEqual(expected_vals.get(var.name), var.val, 5)
