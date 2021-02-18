from lib.std.builtins import binds
from backend.interpreter.eval import evaluate
from backend.interpreter.internal_tokens import Token, Variable


class Scope:
    def __init__(self, init_vars=None):
        if init_vars is None:
            init_vars = {}

        self.variables = {**binds, **init_vars}

    def get(self, var):
        if isinstance(var, Variable):
            return get_var(self, var)
        elif not isinstance(var, str):
            return evaluate(var)

        return self.variables[var]


def get_var(this_scope, var):
    scope = this_scope

    for pathelement in var.value:
        scope = scope.get(pathelement)

        # TODO: rewrite this shit
        if isinstance(scope, Token):
            scope = scope.scope

    return scope    # scope is a value (I hope)
