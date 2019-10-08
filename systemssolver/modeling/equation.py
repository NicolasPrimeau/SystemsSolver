from enum import Enum
from typing import List

from systemssolver.modeling import Term, Coefficient


class EqualitySigns(Enum):
    EQUAL = '='
    LT = '<'
    LE = '<='
    GT = '>'
    GE = '>='
    NOT_EQUAL = '!='

    def apply(self, right, left) -> bool:
        return {
            EqualitySigns.EQUAL: lambda r, l: r == l,
            EqualitySigns.LT: lambda r, l: r < l,
            EqualitySigns.LE: lambda r, l: r <= l,
            EqualitySigns.GT: lambda r, l: r > l,
            EqualitySigns.GE: lambda r, l: r >= l,
            EqualitySigns.NOT_EQUAL: lambda r, l: r != l
        }[self](right, left)

    def __str__(self):
        return self.value


class Expression:

    def __init__(self, terms: List[Term] = None):
        self._vars = terms if terms else list()

    def add_term(self, term: Term):
        self._vars.append(term)

    @property
    def terms(self) -> List[Term]:
        return self._vars

    def evaluate(self):
        total = 0
        for term in self._vars:
            value = term.evaluate()
            if not value:
                return None
            total += value
        return total

    def is_equivalent(self, other) -> bool:
        return set(self.terms) == set(other.terms)

    def simplify(self):
        terms = dict()
        for term in self.terms:
            if term.var not in terms:
                terms[term.var] = 0
            terms[term.var] += term.coef.val
        self._vars = [Term(var=var, coef=Coefficient(val)) for var, val in terms.items()]

    def __str__(self):
        terms = list()
        for term in self.terms:
            if term.coef.val >= 0:
                terms.append("{}{}{}".format("+ " if len(terms) > 0 else "", term.coef.val, term.var.name))
            else:
                terms.append("- {}{}".format(abs(term.coef.val), term.var.name))
        return ' '.join(terms)

    def __neg__(self):
        return Expression([-term for term in self.terms])

    def __eq__(self, other):
        if not isinstance(other, Expression):
            return False
        return self.evaluate() == other.evaluate()

    def __lt__(self, other):
        if not isinstance(other, Expression):
            return False
        return self.evaluate() < other.evaluate()

    def __le__(self, other):
        if not isinstance(other, Expression):
            return False
        return self.evaluate() <= other.evaluate()

    def __gt__(self, other):
        if not isinstance(other, Expression):
            return False
        return self.evaluate() > other.evaluate()

    def __ge__(self, other):
        if not isinstance(other, Expression):
            return False
        return self.evaluate() >= other.evaluate()

    def __ne__(self, other):
        if not isinstance(other, Expression):
            return False
        return self.evaluate() != other.evaluate()


class Constraint:

    def __init__(self, left: Expression, right: Expression, sign: EqualitySigns):
        self.left, self.right, self._sign = left, right, sign

    def is_satisfied(self):
        return self._sign.apply(self.left, self.right)

    def __str__(self):
        return str(self.left) + " " + str(self._sign) + " " + str(self.right)
