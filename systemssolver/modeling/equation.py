from enum import Enum
from typing import List, Dict

from systemssolver.modeling.variables import Term


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
        self._terms = terms if terms else list()

    def add_term(self, term: Term):
        self._terms.append(term)

    @property
    def terms(self) -> List[Term]:
        return self._terms

    @property
    def coefficients(self) -> List:
        return [term.coef for term in self.terms]

    def var_coef_view(self) -> Dict:
        self.simplify()
        return {term.var: term.coef for term in self.terms}

    def evaluate(self):
        total = 0
        for term in self._terms:
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
                terms[term.var] = term.coef
            terms[term.var] += term.coef
        self._terms = [Term(var=var, coef=coef) for var, coef in terms.items()]

    def copy(self):
        return Expression([term.copy() for term in self.terms])

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

    def __add__(self, other):
        if isinstance(other, Term):
            terms = [term.copy() for term in self.terms]
            terms.append(other)
            exp = Expression(terms)
            exp.simplify()
            return exp
        elif isinstance(other, Expression):
            terms = [term.copy() for term in self.terms]
            terms.extend(other.terms)
            exp = Expression(terms)
            exp.simplify()
            return exp
        raise NotImplementedError()

    def __sub__(self, other):
        if isinstance(other, Term):
            exp = self.copy()
            var_coefs = exp.var_coef_view()

            if other.var not in var_coefs:
                var_coefs[other.var] = -other.coef
            else:
                var_coefs[other.var] -= other.coef
            exp._terms = [Term(var=var, coef=coef) for var, coef in var_coefs.items()]
            return exp
        elif isinstance(other, Expression):
            exp = self.copy()
            var_coefs = exp.var_coef_view()
            for var, item in other.var_coef_view().items():
                if var not in var_coefs:
                    var_coefs[var] = 0
                var_coefs[var] -= item
            exp._terms = [Term(var=var, coef=coef) for var, coef in var_coefs.items()]
            return exp
        raise NotImplementedError()

    def __mul__(self, other):
        terms = [term.copy() for term in self.terms]
        for term in terms:
            term.coef *= other
        return self

    def __truediv__(self, other):
        terms = [term.copy() for term in self.terms]
        for term in terms:
            term.coef /= other
        return self

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
        self.left: Expression = left
        self.right: Expression = right
        self.sign = sign

    def is_satisfied(self):
        return self.sign.apply(self.left, self.right)

    def __str__(self):
        return str(self.left) + " " + str(self.sign) + " " + str(self.right)


def convert_constraint_to(constraint: Constraint, sign: EqualitySigns):
    if constraint.sign == sign:
        return constraint
    raise NotImplementedError()
