from enum import Enum

from systemssolver.modeling.equation import Expression


class ObjectiveGoal(Enum):
    MINIMIZE = 'minimize'
    MAXIMIZE = 'maximize'


class Objective:

    def __init__(self, expression: Expression, goal: ObjectiveGoal):
        self._expression, self._goal = expression, goal

    @property
    def expression(self) -> Expression:
        return self._expression

    @property
    def goal(self) -> ObjectiveGoal:
        return self._goal

    def __eq__(self, other):
        return isinstance(other, Objective) and self.expression == other.expression and other.goal == self.goal


def convert_min_objective_to_max(obj: Objective) -> Objective:
    if obj.goal == ObjectiveGoal.MAXIMIZE:
        return obj
    return Objective(expression=-obj.expression, goal=ObjectiveGoal.MAXIMIZE)
