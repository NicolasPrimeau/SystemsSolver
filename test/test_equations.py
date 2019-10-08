import unittest

from systemssolver.solver.modeling.equation import Expression, Constraint, EqualitySigns
from systemssolver.solver.modeling.variables import Term, Variable, Coefficient, Constant


class EquationsTest(unittest.TestCase):

    def test_expression(self):
        expression = Expression()
        expression.add_term(Term(var=Variable('a', 2)))
        expression.add_term(Term(var=Variable('b', 5), coef=Coefficient(-2)))
        expression.add_term(Term(var=Variable('c', 4), coef=Coefficient(5)))
        val = expression.evaluate()
        print(str(expression))
        self.assertEqual(2 - 2 * 5 + 5 * 4, val)

    def test_constraints(self):
        expression = Expression()
        expression.add_term(Term(var=Variable('a', 2)))
        expression.add_term(Term(var=Variable('b', 5), coef=Coefficient(-2)))
        expression.add_term(Term(var=Variable('c', 4), coef=Coefficient(5)))

        constraint = Constraint(left=expression, right=Expression(terms=[
            Term(var=Constant(name='constraint1', val=12))
        ]), sign=EqualitySigns.LE)

        self.assertTrue(constraint.is_satisfied())

    def test_constraints2(self):
        expression = Expression()
        expression.add_term(Term(var=Variable('a', 2)))
        expression.add_term(Term(var=Variable('b', 5), coef=Coefficient(-2)))
        expression.add_term(Term(var=Variable('c', 4), coef=Coefficient(5)))

        constraint = Constraint(left=expression, right=Expression(terms=[
            Term(var=Constant(name='constraint1', val=12))
        ]), sign=EqualitySigns.LT)

        self.assertFalse(constraint.is_satisfied())