import unittest

from systemssolver.modeling.parsing import ExpressionParser
from systemssolver.modeling.variables import Term, Variable


class ExpressionParserTest(unittest.TestCase):

    def test_parse_simple_expression(self):
        parser = ExpressionParser()
        expression = parser.parse("x")
        self.assertEqual(1, len(expression.terms))
        self.assertEqual(Term(coef=1, var=Variable(name='x')), expression.terms[0])

    def test_coef(self):
        parser = ExpressionParser()
        expression = parser.parse("3x")
        self.assertEqual(1, len(expression.terms))
        self.assertEqual(Term(coef=3, var=Variable(name='x')), expression.terms[0])

    def test_multi_term(self):
        parser = ExpressionParser()
        expression = parser.parse("3x - 5y")
        self.assertEqual(2, len(expression.terms))
        self.assertEqual(Term(coef=3, var=Variable(name='x')), expression.terms[0])
        self.assertEqual(Term(coef=-5, var=Variable(name='y')), expression.terms[1])

    def test_constant(self):
        parser = ExpressionParser()
        expression = parser.parse("3x - 5y + 5")
        self.assertEqual(3, len(expression.terms))
        self.assertEqual(Term(coef=3, var=Variable(name='x')), expression.terms[0])
        self.assertEqual(Term(coef=-5, var=Variable(name='y')), expression.terms[1])
        self.assertEqual(Term(coef=5), expression.terms[2])

    def test_no_coef(self):
        parser = ExpressionParser()
        expression = parser.parse("3x - y + 5")
        self.assertEqual(3, len(expression.terms))
        self.assertEqual(Term(coef=3, var=Variable(name='x')), expression.terms[0])
        self.assertEqual(Term(coef=-1, var=Variable(name='y')), expression.terms[1])
        self.assertEqual(Term(coef=5), expression.terms[2])

    def test_starting_const(self):
        parser = ExpressionParser()
        expression = parser.parse("-5")
        self.assertEqual(1, len(expression.terms))
        self.assertEqual(Term(coef=-5), expression.terms[0])
