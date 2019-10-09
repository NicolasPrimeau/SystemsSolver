from enum import Enum


class VariableType(Enum):
    INTEGER = 'integer'
    REAL = 'real'


class Variable:

    def __init__(self, name, val=None, vtype=VariableType.REAL, inverted=False):
        self._val, self._name, self._type, self._inverted = val, name, vtype, inverted

    @property
    def name(self):
        return self._name

    @property
    def val(self):
        return self._val if not self._inverted else -self._val

    @val.setter
    def val(self, new_val):
        self._val = new_val

    def __eq__(self, other):
        return isinstance(other, Variable) and other.name == self.name

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return self.name


class Constant(Variable):

    def __init__(self, name, val):
        super().__init__(name, val)

    @property
    def val(self):
        return self._val

    @val.setter
    def val(self, new_val):
        raise RuntimeError()

    @property
    def name(self):
        return self.val

    def __str__(self):
        return str(self.val) if self.val >= 0 else '-{}'.format(self.val)


class Term:

    def __init__(self, var: Variable, coef=1):
        self.var: Variable = var
        self.coef = coef

    def evaluate(self):
        if not self.var.val:
            return None
        return self.var.val * self.coef

    def copy(self):
        return Term(var=self.var, coef=self.coef)

    def __hash__(self):
        return hash((self.var, self.coef))

    def __eq__(self, other):
        return isinstance(other, Term) and other.var == self.var and other.coef == self.coef

    def __neg__(self):
        return Term(var=self.var, coef=-self.coef)

    def __str__(self):
        if self.coef != 1:
            return str(self.var)
        else:
            return "{}*{}".format(str(self.coef), str(self.var))
