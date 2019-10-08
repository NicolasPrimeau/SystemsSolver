from systemssolver.solution import Solution


class TracingHook:

    def step(self, solution: Solution):
        pass


class PrintSolutionHook(TracingHook):

    def step(self, solution: Solution):
        print(str(solution))
