from core.objects.types import FUNCTION, FUNCTION_CALL, VARASSIGN


function_form = """def {name}({args}):
    {code}"""
function_call_form = "{name}({args})"
varassign_form = "{var} = {val}"


forms = {
    FUNCTION: function_form,
    FUNCTION_CALL: function_call_form,
    VARASSIGN: varassign_form,
}
