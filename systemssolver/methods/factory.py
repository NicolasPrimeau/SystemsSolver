from enum import Enum

from systemssolver.methods.simplex import SimplexSolver
from systemssolver.methods.solvermethod import SolverMethod


class SolverMethods(Enum):
    SIMPLEX = 'simplex'

    @staticmethod
    def from_val(val):
        for method in SolverMethods:
            if method.value == val.lower():
                return method
        return None

    def get_solver(self) -> SolverMethod:
        return {
            SolverMethods.SIMPLEX: SimplexSolver
        }[self]()
