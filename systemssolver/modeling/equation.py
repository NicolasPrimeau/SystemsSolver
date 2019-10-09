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

    @staticmethod
    def from_val(val):
        for sign in EqualitySigns:
            if sign.value == val:
                return sign
        return None

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
        var_coefs = dict()
        for term in self.terms:
            search_key = term.var if term.var is not None else 'constant'
            var_coefs[search_key] = term.coef
        return var_coefs

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
            search_key = term.var if term.var is not None else 'constant'
            if search_key not in terms:
                terms[search_key] = 0
            terms[search_key] += term.coef
        self._terms = [Term(var=var, coef=coef) for var, coef in terms.items()]

    def copy(self):
        return Expression([term.copy() for term in self.terms])

    def __str__(self):
        terms = list()
        for term in self.terms:
            encoded = ""
            if len(terms) > 0:
                encoded += "+ " if term.coef > 0 else "- "
            elif len(terms) == 0:
                encoded += "" if term.coef > 0 else "- "

            if term.coef != 0:
                if term.var is not None:
                    if term.coef != 1:
                        encoded += str(abs(term.coef))
                    encoded += str(term.var)
                else:
                    encoded += str(abs(term.coef))
                terms.append(encoded)

        if len(terms) == 0:
            return '0'
        return ' '.join(terms)

    def __neg__(self):
        return Expression([-term for term in self.terms])

    def __add__(self, other):
        if isinstance(other, Term):
            exp = self.copy()
            var_coefs = exp.var_coef_view()
            search_key = other.var if other.var is not None else 'constant'

            if search_key not in var_coefs:
                var_coefs[search_key] = other.coef
            else:
                var_coefs[search_key] += other.coef
            if var_coefs[search_key] == 0:
                var_coefs.pop(search_key)

            terms = list()
            for var, coef in var_coefs.items():
                if var != 'constant':
                    terms.append(Term(coef=coef, var=var))
                else:
                    terms.append(Term(coef=coef))
            exp._terms = terms
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

            search_key = other.var if other.var is not None else 'constant'

            if search_key not in var_coefs:
                var_coefs[search_key] = -other.coef
            else:
                var_coefs[search_key] -= other.coef

            if var_coefs[search_key] == 0:
                var_coefs.pop(search_key)

            terms = list()
            for var, coef in var_coefs.items():
                if var != 'constant':
                    terms.append(Term(coef=coef, var=var))
                else:
                    terms.append(Term(coef=coef))
            exp._terms = terms
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


def convert_constraint_to(constraint: Constraint, sign: EqualitySigns) -> Constraint:
    if constraint.sign == sign:
        return constraint

    if sign == EqualitySigns.LE:
        if constraint.sign == EqualitySigns.LT:
            return Constraint(left=constraint.left, right=constraint.right, sign=EqualitySigns.LE)
        elif constraint.sign == EqualitySigns.GE:
            return Constraint(left=-constraint.left, right=-constraint.right, sign=EqualitySigns.LE)
        elif constraint.sign == EqualitySigns.GT:
            return Constraint(left=-constraint.left, right=-constraint.right, sign=EqualitySigns.LE)

    if sign == EqualitySigns.LT:
        if constraint.sign == EqualitySigns.LE:
            return Constraint(left=constraint.left, right=constraint.right, sign=EqualitySigns.LT)
        elif constraint.sign == EqualitySigns.GE:
            return Constraint(left=-constraint.left, right=-constraint.right, sign=EqualitySigns.LT)
        elif constraint.sign == EqualitySigns.GT:
            return Constraint(left=-constraint.left, right=-constraint.right, sign=EqualitySigns.LT)

    if sign == EqualitySigns.GE:
        if constraint.sign == EqualitySigns.GT:
            return Constraint(left=constraint.left, right=constraint.right, sign=EqualitySigns.GE)
        elif constraint.sign == EqualitySigns.LE:
            return Constraint(left=-constraint.left, right=-constraint.right, sign=EqualitySigns.GE)
        elif constraint.sign == EqualitySigns.LT:
            return Constraint(left=-constraint.left, right=-constraint.right, sign=EqualitySigns.GE)

    if sign == EqualitySigns.GT:
        if constraint.sign == EqualitySigns.GE:
            return Constraint(left=constraint.left, right=constraint.right, sign=EqualitySigns.GT)
        elif constraint.sign == EqualitySigns.LE:
            return Constraint(left=-constraint.left, right=-constraint.right, sign=EqualitySigns.GT)
        elif constraint.sign == EqualitySigns.LT:
            return Constraint(left=-constraint.left, right=-constraint.right, sign=EqualitySigns.GT)
    raise NotImplementedError()
