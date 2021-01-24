from core.objects.tools import split_tokens
from core.objects.types import COMMA, VARASSIGN, EXPR
from core.objects.classes import (Function, FunctionCall, VarAssign,
                                  ReturnStatement, IfBranchLeaf, ElifBranchLeaf,
                                  ElseBranchLeaf)


def function(parser, tokens):
    _, name, raw_args, raw_body = tokens
    body = parser(raw_body.value)
    args, kwargs = _parse_args(parser, raw_args.value)

    return Function(name.value, args, kwargs, body)


def function_call(parser, tokens):
    name, raw_args = tokens
    args, kwargs = _parse_args(parser, raw_args.value)

    return FunctionCall(name.value, args, kwargs)


def var_assign(parser, tokens):
    var, _, *raw_val = tokens
    val = parser(raw_val)[0]

    if val.type == EXPR:
        val = val.value[0]

    return VarAssign(var, val)


def if_branch(parser, tokens):
    _, expr, raw_body = tokens
    body = parser(raw_body.value)

    return IfBranchLeaf(expr.value, body)


def elif_branch(parser, tokens):
    _, expr, raw_body = tokens
    body = parser(raw_body.value)

    return ElifBranchLeaf(expr.value, body)


def else_branch(parser, tokens):
    _, raw_body = tokens
    body = parser(raw_body.value)

    return ElseBranchLeaf(body)


def return_statement(parser, tokens):
    _, *raw_value = tokens
    value = parser(raw_value)[0]

    return ReturnStatement(value)


def _parse_args(parser, args, leave_tokens=True):
    if not args:
        return [], {}

    elements = split_tokens(args, COMMA)
    args = []
    kwargs = {}

    for element in elements:
        parsed_element = parser(element)[0]

        if parsed_element.type != VARASSIGN:    # to accept all the structures inside
            arg = parsed_element.value[0]

            if not leave_tokens:
                arg = arg.value

            args.append(arg)
        else:   # this is kwarg
            val = element.val

            if not leave_tokens:
                val = val.value

            kwargs[element.var.value] = val

    return args, kwargs
