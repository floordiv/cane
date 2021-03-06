from core.objects import types


MINIMAL_PRIORITY = 0
QUARTER_PRIORITY = 1
MIDDLE_PRIORITY = 2
MAXIMAL_PRIORITY = 3


TOKENS_PRIORITIES = {
    types.EQEQUALS: MINIMAL_PRIORITY,
    types.IS: MINIMAL_PRIORITY,
    types.NOTIS: MINIMAL_PRIORITY,

    types.PLUS: QUARTER_PRIORITY,
    types.MINUS: QUARTER_PRIORITY,
}
