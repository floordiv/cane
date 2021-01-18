from core.objects.types import (ANY, FUNCTION_CALL, FUNCTION,
                                VARASSIGN)


class Token:
    def __init__(self, typeof, value, primary_type=None,
                 unary=None):
        self.type = typeof
        self.primary_type = primary_type or typeof
        self.value = value
        self.unary = unary

    def __str__(self):
        return f'{self.type}(value={repr(self.value)})'

    __repr__ = __str__


class MatchToken:
    """
    token for semantic to match constructions
    """
    
    def __init__(self, *types):
        self.types = types

    def match(self, token: Token):
        return (ANY in self.types) or (token.type in self.types) or (token.primary_type in self.types)

    def __str__(self):
        return f'MatchToken({", ".join(self.types)})'

    __repr__ = __str__


class FunctionCall(Token):
    def __init__(self, name, args, kwargs):
        super(FunctionCall, self).__init__(FUNCTION_CALL, name)

        self.name = name
        self.args = args
        self.kwargs = kwargs


class Function(Token):
    def __init__(self, name, args, kwargs, code):
        super(Function, self).__init__(FUNCTION, name)

        self.name = name
        self.args = args
        self.kwargs = kwargs
        self.code = code


class VarAssign(Token):
    def __init__(self, var, val):
        super(VarAssign, self).__init__(VARASSIGN, var)

        self.var = var.value
        self.val = val

    def __str__(self):
        return f'VarAssign({self.var} = {repr(self.val)})'

    __repr__ = __str__
