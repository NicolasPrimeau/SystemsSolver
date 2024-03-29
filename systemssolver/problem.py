from typing import List, Set, Dict

from systemssolver.modeling.equation import Constraint, Expression
from systemssolver.modeling.objective import Objective
from systemssolver.modeling.variables import Variable


class Problem:

    def __init__(self):
        self._objective_functions: List[Objective] = list()
        self._constraints: List[Constraint] = list()
        self._variables: Dict[Variable, Variable] = dict()

    def add_objective(self, obj: Objective):
        self._update_variable(obj.expression)
        self._objective_functions.append(obj)

    def add_constraint(self, obj: Constraint):
        self._update_variable(obj.right)
        self._update_variable(obj.left)
        self._constraints.append(obj)

    def _update_variable(self, expression: Expression):
        for term in expression.terms:
            if term.var is not None and term.var not in self._variables:
                self._variables[term.var] = term.var
            elif term.var in self._variables:
                term.var = self._variables[term.var]

    def set_variable(self, variable: Variable):
        must_update = variable in self._variables
        must_switch = False
        if must_update:
            old_var = self._variables.pop(variable)
            must_switch = old_var.is_inverted != variable.is_inverted

        self._variables[variable] = variable
        if must_update:
            for objective in self.objectives:
                self._update_variable(objective.expression)
            for constraint in self._constraints:
                self._update_variable(constraint.left)
                self._update_variable(constraint.right)

        if must_switch:
            for objective in self.objectives:
                self._flip_terms(objective.expression, variable)

            for constraint in self._constraints:
                self._flip_terms(constraint.left, variable)
                self._flip_terms(constraint.right, variable)

    def _flip_terms(self, expression: Expression, variable: Variable):
        for term in expression.terms:
            if term.var == variable:
                term.coef *= -1

    @property
    def objectives(self) -> List[Objective]:
        return self._objective_functions

    @property
    def constraints(self) -> List[Constraint]:
        return self._constraints

    @property
    def variables(self) -> Set[Variable]:
        return set(self._variables.keys())
