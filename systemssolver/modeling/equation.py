from enum import Enum
from typing import List, Dict

from systemssolver.modeling.variables import Coefficient, Term, Variable


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
    def coefficients(self) -> List[Coefficient]:
        return [term.coef for term in self.terms]

    def var_coef_view(self) -> Dict[Variable, Coefficient]:
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
        if isinstance(other, Coefficient):
            for coef in self.coefficients:
                coef.val = coef.val + other.val
            return self
        elif isinstance(other, Expression):
            self.terms.extend(other.terms)
            self.simplify()
            return self
        raise NotImplementedError()

    def __sub__(self, other):
        if isinstance(other, Coefficient):
            for coef in self.coefficients:
                coef.val = coef.val - other.val
            return self
        elif isinstance(other, Expression):
            var_coefs = self.var_coef_view()
            for var, item in other.var_coef_view().items():
                if var not in var_coefs:
                    var_coefs[var] = Coefficient(val=0)
                var_coefs[var] -= item
            self._terms = [Term(var=var, coef=coef) for var, coef in var_coefs.items()]
            return self
        raise NotImplementedError()

    def __mul__(self, other):
        for coef in self.coefficients:
            coef.val *= other
        return self

    def __truediv__(self, other):
        for coef in self.coefficients:
            coef /= other
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
        self.left, self.right, self.sign = left, right, sign

    def is_satisfied(self):
        return self.sign.apply(self.left, self.right)

    def __str__(self):
        return str(self.left) + " " + str(self.sign) + " " + str(self.right)


def convert_constraint_to(constraint: Constraint, sign: EqualitySigns):
    if constraint.sign == sign:
        return constraint
    pass
