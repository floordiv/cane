import core.objects.types as types


class ExecuteCode:
    """
    Used in interpreter.logic. If function returned
    this class, executor will execute code from this
    class recursively
    """

    def __init__(self, code):
        self.code = code


class Token:
    def __init__(self, scope, typeof, value,
                 primary_type=None, unary=None):
        self.scope = scope
        self.type = typeof
        self.primary_type = primary_type or typeof
        self.value = value
        self.unary = unary

    def __str__(self):
        return f'{self.type}(value={repr(self.value)})'

    __repr__ = __str__


class FunctionCall(Token):
    def __init__(self, scope, name, args, kwargs):
        super(FunctionCall, self).__init__(scope, types.FUNCTION_CALL, name)

        self.name = name
        self.args = args
        self.kwargs = kwargs


class Function(Token):
    def __init__(self, scope, name, args, kwargs, code):
        super(Function, self).__init__(scope, types.FUNCTION, name)

        self.name = name
        self.args = args
        self.kwargs = kwargs
        self.code = code


class VarAssign(Token):
    def __init__(self, scope, var, val):
        super(VarAssign, self).__init__(scope, types.VARASSIGN, var)

        self.var = var.value
        self.val = val

    def __str__(self):
        return f'VarAssign({self.var} = {repr(self.val)})'

    __repr__ = __str__


class VarUnpackingAssign(Token):
    def __init__(self, scope, var, val):
        super(VarUnpackingAssign, self).__init__(scope, types.VARASSIGN, var)

        self.var = var
        self.val = val


class ConditionBranch(Token):
    def __init__(self, scope, if_branch=None):
        super(ConditionBranch, self).__init__(scope, types.CONDITION_BRANCH, if_branch)

        self.if_branch = if_branch
        self.elif_branches = []
        self.else_branch = None


class WhileLoop(Token):
    def __init__(self, scope, expr, body):
        super(WhileLoop, self).__init__(scope, types.WHILE_LOOP, expr)

        self.expr = expr
        self.body = body


class ForLoop(Token):
    def __init__(self, scope, begin, end, step, body):
        super(ForLoop, self).__init__(scope, types.FOR_LOOP, end)

        self.begin = begin
        self.end = end
        self.step = step
        self.body = body


class ReturnStatement(Token):
    def __init__(self, scope, value):
        super(ReturnStatement, self).__init__(scope, types.RETURN_STATEMENT, value)


class ContinueStatement(Token):
    def __init__(self):
        super(ContinueStatement, self).__init__(None, types.CONTINUE_STATEMENT, None)


class BreakStatement(Token):
    def __init__(self):
        super(BreakStatement, self).__init__(None, types.BREAK_STATEMENT, None)


class ImportStatement(Token):
    def __init__(self, scope, package_path, import_as):
        super(ImportStatement, self).__init__(scope, types.IMPORT_STATEMENT, package_path)

        self.path = package_path
        self.import_as = import_as


class Variable(Token):
    def __init__(self, scope, path):
        super(Variable, self).__init__(scope, types.VARIABLE, path)

