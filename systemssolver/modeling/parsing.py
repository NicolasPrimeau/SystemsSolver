from systemssolver.modeling.equation import Expression
from systemssolver.modeling.variables import Term, Variable, Constant


class ExpressionParser:

    def parse(self, encoded: str) -> Expression:
        si = None
        co = None
        var = None

        def get_var(sign, coef, var_name):
            if sign is not None and coef is not None and var_name is not None:
                val = float('{}{}'.format(sign, coef))
                return Term(coef=val, var=Variable(var_name))
            elif sign is not None and coef is not None:
                val = float('{}{}'.format(sign, coef))
                return Term(var=Constant(name='constant{}'.format(str(len(terms))), val=val))
            elif coef is not None and var_name is not None:
                return Term(coef=float(coef), var=Variable(var_name))
            elif sign is not None and var_name is not None:
                return Term(var=Variable(name=var_name), coef=1 if sign == '+' else -1)
            elif coef is not None:
                return Term(var=Constant(name='constant{}'.format(str(len(terms))), val=float(coef)))
            elif var_name is not None:
                return Term(var=Variable(name=var_name))
            return None
        terms = list()
        for char in encoded:
            if char == ' ':
                term = get_var(si, co, var)
                if term:
                    terms.append(term)
                    si = var = co = None
            elif char == '+' or char == '-':
                si = char
            elif char.isalpha():
                var = char
            elif char.isalnum():
                co = char
        else:
            term = get_var(si, co, var)
            if term:
                terms.append(term)
        return Expression(terms=terms)
