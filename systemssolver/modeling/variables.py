class Variable:

    def __init__(self, name, val=None):
        self._val = val
        self._name = name

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

    def __str__(self):
        return str(self.val) if self.val >= 0 else '-{}'.format(self.val)


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

    def __str__(self):
        if self.coef.val != 1:
            return str(self.var)
        else:
            return "{}*{}".format(str(self.coef), str(self.var))
