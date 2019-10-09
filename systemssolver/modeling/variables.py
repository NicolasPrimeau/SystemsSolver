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

    @property
    def is_inverted(self):
        return self._inverted

    @property
    def var_type(self):
        return self._type

    @val.setter
    def val(self, new_val):
        self._val = new_val

    def __eq__(self, other):
        return isinstance(other, Variable) and other.name == self.name

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return self.name


class Term:

    def __init__(self, var: Variable = None, coef=None):
        self._var: Variable = var
        if var is None and coef is None:
            self.coef = 0
        elif var is not None and coef is None:
            self.coef = 1
        else:
            self.coef = coef

    @property
    def var(self):
        return self._var

    @var.setter
    def var(self, new_val: Variable):
        self._var = new_val

    def evaluate(self):
        if self.var is None:
            return self.coef
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
        if self.var is None:
            return str(self.coef)

        if self.coef == 1:
            return str(self.var)
        else:
            return "{}*{}".format(str(self.coef), str(self.var))
