from typing import Iterable

from core.transpiler.python.forms import (function_form, function_call_form, varassign_form,
                                          return_form, if_branch_form, elif_branch_form, else_branch_form,)
from core.objects.types import (FUNCTION_CALL, FUNCTION, VARASSIGN,
                                RETURN_STATEMENT, EXPR, INTEGER,
                                FLOAT, STRING, BOOL, VARIABLE)


def function_call(source_gen, token, indent):
    args = _get_string_with_args(token.args, token.kwargs)

    return function_call_form.format(name=token.name, args=args)


def function(source_gen, token, indent):
    function_args = _get_string_with_args(token.args, token.kwargs)
    function_body = source_gen(token.code, indent=indent + 1)

    return function_form.format(name=token.name, args=function_args, code=function_body)


def varassign(source_gen, token, indent):
    return varassign_form.format(var=token.var, val=source_gen([token.val]))


def branch(source_gen, token, indent):
    if_branch = token.if_branch
    if_branch_expr = expr(source_gen, if_branch.expr, indent)
    if_branch_body = source_gen(if_branch.body)
    whole_branch = if_branch_form.format(expr=if_branch_expr, code=if_branch_body) + '\n'

    for elif_branch in token.elif_branches:
        elif_branch_expr = expr(source_gen, elif_branch.expr, indent)
        elif_branch_body = source_gen(elif_branch.body)
        whole_branch += elif_branch_form.format(expr=elif_branch_expr, code=elif_branch_body) + '\n'

    if token.else_branch:
        whole_branch += else_branch_form.format(code=source_gen(token.else_branch.body)) + '\n'

    return whole_branch


def return_statement(source_gen, token, indent):
    value = token.value

    if not isinstance(value, Iterable):
        value = (value,)

    return return_form.format(val=source_gen(value))


def expr(source_gen, token, indent):
    elements = []

    for element in token.value:
        if element.type == FUNCTION_CALL:
            elements.append(function_call(source_gen, element, indent))
        else:
            elements.append(str(element.value))

    return ' '.join(elements)


def valueof(source_gen, token, indent):
    return str(token.value)


def _get_string_with_args(args, kwargs):
    if args:
        args = ', '.join(_get_value(arg) for arg in args)
    else:
        args = ''

    if kwargs:
        kwargs = ', '.join(f'{kwvar}={kwval}' for kwvar, kwval in kwargs)
    else:
        kwargs = ''

    if args and kwargs:
        args += ', '

    return args + kwargs


def _get_value(token):
    if token.type == VARIABLE:
        return token.value
    elif token.type == STRING:
        return repr(token.value)

    return str(token.value)


builders = {
    FUNCTION_CALL: function_call,
    FUNCTION: function,
    VARASSIGN: varassign,
    RETURN_STATEMENT: return_statement,
    EXPR: expr,
    INTEGER: valueof,
    FLOAT: valueof,
    STRING: valueof,
    BOOL: valueof,
}
