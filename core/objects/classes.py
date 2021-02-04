import core.objects.types as types


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
    
    def __init__(self, *token_types):
        self.types = token_types

    def match(self, token: Token):
        return (types.ANY in self.types) or (token.type in self.types) or (token.primary_type in self.types)

    def __str__(self):
        return f'MatchToken({", ".join(self.types)})'

    __repr__ = __str__


class FunctionCall(Token):
    def __init__(self, name, args, kwargs):
        super(FunctionCall, self).__init__(types.FUNCTION_CALL, name)

        self.name = name
        self.args = args
        self.kwargs = kwargs


class Function(Token):
    def __init__(self, name, args, kwargs, code):
        super(Function, self).__init__(types.FUNCTION, name)

        self.name = name
        self.args = args
        self.kwargs = kwargs
        self.code = code


class VarAssign(Token):
    def __init__(self, var, val):
        super(VarAssign, self).__init__(types.VARASSIGN, var)

        self.var = var.value
        self.val = val

    def __str__(self):
        return f'VarAssign({self.var} = {repr(self.val)})'

    __repr__ = __str__


class IfBranchLeaf(Token):
    def __init__(self, expr, body):
        super(IfBranchLeaf, self).__init__(types.IF_BLOCK, body)

        self.expr = expr
        self.body = body


class ElifBranchLeaf(Token):
    def __init__(self, expr, body):
        super(ElifBranchLeaf, self).__init__(types.ELIF_BLOCK, body)

        self.expr = expr
        self.body = body


class ElseBranchLeaf(Token):
    def __init__(self, body):
        super(ElseBranchLeaf, self).__init__(types.ELSE_BLOCK, body)

        self.body = body


class ConditionBranch(Token):
    def __init__(self, if_branch=None):
        super(ConditionBranch, self).__init__(types.CONDITION_BRANCH, if_branch)

        self.if_branch = if_branch
        self.elif_branches = []
        self.else_branch = None

    def add_elif_branch(self, branch):
        self.elif_branches.append(branch)

    def set_else_branch(self, branch):
        self.else_branch = branch


class WhileLoop(Token):
    def __init__(self, expr, body):
        super(WhileLoop, self).__init__(types.WHILE_LOOP, expr)

        self.expr = expr
        self.body = body


class ForLoop(Token):
    def __init__(self, begin, end, step, body):
        super(ForLoop, self).__init__(types.FOR_LOOP, end)

        self.begin = begin
        self.end = end
        self.step = step
        self.body = body


class ReturnStatement(Token):
    def __init__(self, value):
        super(ReturnStatement, self).__init__(types.RETURN_STATEMENT, value)


class ContinueStatement(Token):
    def __init__(self):
        super(ContinueStatement, self).__init__(types.CONTINUE_STATEMENT, None)


class BreakStatement(Token):
    def __init__(self):
        super(BreakStatement, self).__init__(types.BREAK_STATEMENT, None)


class ImportStatement(Token):
    def __init__(self, package_path, import_as):
        super(ImportStatement, self).__init__(types.IMPORT_STATEMENT, package_path)

        self.path = package_path
        self.import_as = import_as
