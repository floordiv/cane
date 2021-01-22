from core.objects.types import (FUNCTION, FUNCTION_CALL, VARASSIGN,
                                RETURN_STATEMENT)


function_form = """def {name}({args}):\n{code}"""
function_call_form = "{name}({args})\n"
varassign_form = "{var} = {val}"
if_branch_form = "if {expr}:\n{code}"
elif_branch_form = "elif {expr}:\n{code}"
else_branch_form = "else:\n{code}"
return_form = "return {val}\n"


forms = {
    FUNCTION: function_form,
    FUNCTION_CALL: function_call_form,
    VARASSIGN: varassign_form,
    RETURN_STATEMENT: return_form,
}
