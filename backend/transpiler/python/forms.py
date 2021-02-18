import core.objects.types as types

function_form = "def {name}({args}):\n{code}\n"
function_call_form = "{name}({args})\n"
varassign_form = "{var} = {val}\n"
if_branch_form = "if {expr}:\n{code}\n"
elif_branch_form = "elif {expr}:\n{code}\n"
else_branch_form = "else:\n{code}\n"
return_form = "return {val}\n"
break_form = "break"
continue_form = "continue"

forms = {
    types.FUNCTION: function_form,
    types.FUNCTION_CALL: function_call_form,
    types.VARASSIGN: varassign_form,
    types.RETURN_STATEMENT: return_form,
    types.BREAK_STATEMENT: break_form,
    types.CONTINUE_STATEMENT: continue_form
}
