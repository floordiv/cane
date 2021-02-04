import core.objects.classes as classes
from core.objects.tools import split_tokens
from core.objects.types import (COMMA, VARASSIGN, EXPR,
                                COLON, SEMICOLON)


def function(parser, tokens):
    _, name, raw_args, raw_body = tokens
    body = parser(raw_body.value)
    args, kwargs = _parse_args(parser, raw_args.value)

    return classes.Function(name.value, args, kwargs, body)


def function_call(parser, tokens):
    name, raw_args = tokens
    args, kwargs = _parse_args(parser, raw_args.value)

    return classes.FunctionCall(name.value, args, kwargs)


def var_assign(parser, tokens):
    var, _, *raw_val = tokens
    val = parser(raw_val)[0]

    if val.type == EXPR:
        val = val.value[0]

    return classes.VarAssign(var, val)


def if_branch(parser, tokens):
    _, expr, raw_body = tokens
    body = parser(raw_body.value)

    return classes.IfBranchLeaf(expr.value, body)


def elif_branch(parser, tokens):
    _, expr, raw_body = tokens
    body = parser(raw_body.value)

    return classes.ElifBranchLeaf(expr.value, body)


def else_branch(parser, tokens):
    _, raw_body = tokens
    body = parser(raw_body.value)

    return classes.ElseBranchLeaf(body)


def return_statement(parser, tokens):
    _, *raw_value = tokens
    value = parser(raw_value)[0]

    return classes.ReturnStatement(value)


def continue_statement(parser, tokens):
    return classes.ContinueStatement()


def break_statement(parser, tokens):
    return classes.BreakStatement()


def while_loop(parser, tokens):
    _, expr, body = tokens

    return classes.WhileLoop(parser(expr.value), parser(body.value))


def for_loop(parser, tokens):
    _, begin_end_step, body = tokens
    split_begin_end_step = split_tokens(begin_end_step.value, SEMICOLON)

    if len(split_begin_end_step) != 3:
        raise SyntaxError('bad syntax in for-loop expression statement')

    begin, end, step = map(parser, split_begin_end_step)

    return classes.ForLoop(begin, end, step, parser(body.value))


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
