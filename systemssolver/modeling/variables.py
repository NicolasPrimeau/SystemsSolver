from enum import Enum


class VariableType(Enum):
    INTEGER = 'integer'
    REAL = 'real'


class Variable:

    def __init__(self, name, val=None, vtype=VariableType.REAL):
        self._val, self._name, self._type = val, name, vtype

    @property
    def name(self):
        return self._name

    @property
    def val(self):
        return self._val

    @val.setter
    def val(self, new_val):
        self._val = new_val

    def __eq__(self, other):
        return isinstance(other, Variable) and other.name == self.name

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return self.name


class Coefficient:

    def __init__(self, val):
        self._val = val

    @property
    def val(self):
        return self._val

    @val.setter
    def val(self, new_val):
        self._val = new_val

    def __eq__(self, other):
        return isinstance(other, Coefficient) and other.val == self.val

    def __str__(self):
        return str(self.val) if self.val >= 0 else '-{}'.format(self.val)

    def __neg__(self):
        return Coefficient(val=-self.val)


class Constant(Variable):

    def __init__(self, name, val):
        super().__init__(name, val)

    @property
    def val(self):
        return self._val

    @val.setter
    def val(self, new_val):
        raise RuntimeError()

    def __str__(self):
        return str(self.val) if self.val >= 0 else '-{}'.format(self.val)


class Term:

    def __init__(self, var: Variable, coef: Coefficient = None):
        self.var = var
        self.coef = coef if coef else Coefficient(val=1)

    def evaluate(self):
        if not self.var.val:
            return None
        return self.var.val * self.coef.val

    def __hash__(self):
        return hash((self.var, self.coef.val))

    def __eq__(self, other):
        return isinstance(other, Term) and other.var == self.var and other.coef == self.coef

    def __neg__(self):
        return Term(var=self.var, coef=-self.coef)

    def __str__(self):
        if self.coef.val != 1:
            return str(self.var)
        else:
            return "{}*{}".format(str(self.coef), str(self.var))
