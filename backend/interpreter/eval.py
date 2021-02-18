def evaluate(expr, scope=None):
    if scope is None:
        scope = {}

    stack = expr[:]  # copy list to avoid caching expressions after first calculating

    while len(stack) > 1:
        ...


def evaluate_from_stack(stack):
    ...


def get_op_from_stack(stack):
    ...

