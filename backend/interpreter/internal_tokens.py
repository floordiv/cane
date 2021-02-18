from core.objects import classes
import core.objects.types as types
from backend.interpreter.scopes import Scope
from backend.interpreter.exec import execute
from backend.interpreter.eval import evaluate


class ExecuteCode:
    """
    Used in interpreter.logic. If function returned
    this class, executor will execute code from this
    class recursively
    """

    def __init__(self, code):
        self.code = code


class FunctionCall(classes.Token):
    def __init__(self, original_class):
        super(FunctionCall, self).__init__(types.FUNCTION_CALL, original_class.name)

        self.name = original_class.name
        self.args = original_class.args
        self.kwargs = original_class.kwargs
        
    def execute(self, scope):
        func = scope.get(self.name)
        # evaluate every argument. For e.x., to get value of variable
        args = map(lambda item: evaluate(item, scope), self.args)
        # same with kwargs
        kwargs = {key: evaluate(value, scope) for key, value in self.kwargs.items()}

        return func(*args, **kwargs)


class Function(classes.Token):
    def __init__(self, original_class):
        super(Function, self).__init__(types.FUNCTION, original_class.name)

        self.name = original_class.name
        self.args = original_class.args
        self.kwargs = original_class.kwargs
        self.code = original_class.code

        self.expected_args = len(self.args)  # to avoid calling len every function's call

    def execute(self, scope):
        scope.set(self.name, self)

    def __call__(self, *args, **kwargs):
        if len(args) != self.expected_args:
            raise SyntaxError(f'expected {self.expected_args} arguments, but got {len(args)} instead')

        init_scope_with_args = {}

        for function_arg, got_arg in zip(self.args, args):
            init_scope_with_args[function_arg] = got_arg

        for kwarg_key, kwarg_value in self.kwargs.items():
            if kwarg_key in kwargs:
                init_scope_with_args[kwarg_key] = kwargs.pop(kwarg_key)
            else:
                init_scope_with_args[kwarg_key] = kwarg_value

        if kwargs:  # there are some unexpected kwargs
            raise SyntaxError('got unexpected kwargs: ' + str(kwargs))

        scope = Scope(init_vars=init_scope_with_args)
        execute(self.code, scope)


class VarAssign(classes.Token):
    def __init__(self, original_class):
        super(VarAssign, self).__init__(types.VARASSIGN, original_class.var)

        self.var = original_class.var.value
        self.val = original_class.val

    def __str__(self):
        return f'VarAssign({self.var} = {repr(self.val)})'

    __repr__ = __str__


class VarUnpackingAssign(classes.Token):
    def __init__(self, original_class):
        super(VarUnpackingAssign, self).__init__(types.VARASSIGN, original_class.var)

        self.var = original_class.var
        self.val = original_class.val


class ConditionBranch(classes.Token):
    def __init__(self, original_class):
        super(ConditionBranch, self).__init__(types.CONDITION_BRANCH, original_class.if_branch)

        self.if_branch = original_class.if_branch
        self.elif_branches = original_class.elif_branches
        self.else_branch = original_class.else_branch


class WhileLoop(classes.Token):
    def __init__(self, original_class):
        super(WhileLoop, self).__init__(types.WHILE_LOOP, original_class.expr)

        self.expr = original_class.expr
        self.body = original_class.body


class ForLoop(classes.Token):
    def __init__(self, original_class):
        super(ForLoop, self).__init__(types.FOR_LOOP, original_class.end)

        self.begin = original_class.begin
        self.end = original_class.end
        self.step = original_class.step
        self.body = original_class.body


class ReturnStatement(classes.Token):
    def __init__(self, original_class):
        super(ReturnStatement, self).__init__(types.RETURN_STATEMENT, original_class.value)


class Variable(classes.Token):
    def __init__(self, original_class):
        super(Variable, self).__init__(types.VARIABLE, original_class.path)


original_tokens2internal = {
    classes.Token: classes.Token,
    classes.FunctionCall: FunctionCall,
    classes.Function: Function,
    classes.VarAssign: VarAssign,
    classes.VarUnpackingAssign: VarUnpackingAssign,
    classes.ConditionBranch: ConditionBranch,
    classes.WhileLoop: WhileLoop,
    classes.ForLoop: ForLoop,
    classes.Variable: Variable,
}

