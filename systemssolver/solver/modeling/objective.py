from enum import Enum

from systemssolver.solver.modeling.equation import Expression


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
