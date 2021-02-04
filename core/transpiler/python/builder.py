from typing import Iterable

import core.transpiler.python.forms as forms
import core.objects.types as types


def function_call(source_gen, token, indent):
    args = _get_string_with_args(token.args, token.kwargs)

    return forms.function_call_form.format(name=token.name, args=args)


def function(source_gen, token, indent):
    function_args = _get_string_with_args(token.args, token.kwargs)
    function_body = source_gen(token.code, indent=indent + 1)

    return forms.function_form.format(name=token.name, args=function_args, code=function_body)


def varassign(source_gen, token, indent):
    return forms.varassign_form.format(var=token.var, val=source_gen([token.val]))


def branch(source_gen, token, indent):
    if_branch = token.if_branch
    if_branch_expr = expr(source_gen, if_branch.expr, indent, from_token=False)
    if_branch_body = source_gen(if_branch.body, indent=indent + 1)
    whole_branch = forms.if_branch_form.format(expr=if_branch_expr, code=if_branch_body)

    for elif_branch in token.elif_branches:
        elif_branch_expr = expr(source_gen, elif_branch.expr, indent, from_token=False)
        elif_branch_body = source_gen(elif_branch.body, indent=indent + 1)
        whole_branch += forms.elif_branch_form.format(expr=elif_branch_expr, code=elif_branch_body)

    if token.else_branch:
        whole_branch += forms.else_branch_form.format(code=source_gen(token.else_branch.body,
                                                                      indent=indent + 1))

    return whole_branch


def return_statement(source_gen, token, indent):
    value = token.value

    if not isinstance(value, Iterable):
        value = (value,)

    return forms.return_form.format(val=source_gen(value))


def break_statement(source_gen, token, indent):
    ...


def continue_statement(source_gen, token, indent):
    ...


def expr(source_gen, values, indent, from_token=True):
    if from_token:
        values = values.value

    elements = []

    for element in values:
        if element.type == types.FUNCTION_CALL:
            elements.append(function_call(source_gen, element, indent))
        elif element.type == types.EXPR:
            elements.append(expr(source_gen, element, indent))
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
    if token.type == types.VARIABLE:
        return token.value
    elif token.type == types.STRING:
        return repr(token.value)

    return str(token.value)


builders = {
    types.FUNCTION_CALL: function_call,
    types.FUNCTION: function,
    types.VARASSIGN: varassign,
    types.RETURN_STATEMENT: return_statement,
    types.EXPR: expr,
    types.INTEGER: valueof,
    types.FLOAT: valueof,
    types.STRING: valueof,
    types.BOOL: valueof,
    types.CONDITION_BRANCH: branch,
}
