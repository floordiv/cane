from core.objects.classes import Variable
from core.interpreter.eval import evaluate


class Scope:
    def __init__(self, init_vars=None):
        if init_vars is None:
            init_vars = {}

        self.variables = init_vars

    def get(self, var):
        if isinstance(var, Variable):
            return get_var(var)
        elif not isinstance(var, str):
            return evaluate(var)

        return self.variables[var]


def get_var(var):
    ...
