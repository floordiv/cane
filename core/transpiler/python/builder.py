from core.transpiler.python.forms import (function_form, function_call_form, varassign_form)


def function_call(token):
    args = _get_string_with_args(token.args, token.kwargs)

    return function_call_form.format(name=token.name, args=args)


def function(token):
    function_args = _get_string_with_args(token.args, token.kwargs)

    return function_form.format(name=token.name, args=function_args, code=token.code)


def varassign(token):
    return varassign_form.format(var=token.var, val=token.val)


def _get_string_with_args(args, kwargs):
    if args:
        args = ', '.join(args)
    if kwargs:
        kwargs = ', '.join(f'{kwvar}={kwval}' for kwvar, kwval in kwargs)

    if args and kwargs:
        args += ', '

    return args + kwargs
