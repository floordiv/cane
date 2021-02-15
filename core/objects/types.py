from core.objects.characters import characters


NO_TYPE = 'NO_TYPE'
INTEGER = 'INTEGER'
FLOAT = 'FLOAT'
STRING = 'STRING'
BOOL = 'BOOL'
VARIABLE = 'VARIABLE'
OPERATOR = 'OPERATOR'

FUNCTION = 'FUNCTION'
FUNCTION_CALL = 'FUNCTION_CALL'
VARASSIGN = 'VARASSIGN'
VARUNPACKASSIGN = 'VARUNPACKASSIGN'
RETURN_STATEMENT = 'RETURN_STATEMENT'
BREAK_STATEMENT = 'BREAK_STATEMENT'
CONTINUE_STATEMENT = 'CONTINUE_STATEMENT'
EXPR = 'EXPR'   # function calls, math operations, etc.
IF_BLOCK = 'IF_BLOCK'
ELIF_BLOCK = 'ELIF_BLOCK'
ELSE_BLOCK = 'ELSE_BLOCK'
CONDITION_BRANCH = 'CONDITION_BRANCH'   # summary for 3 previous class-types
WHILE_LOOP = 'WHILE_LOOP'
FOR_LOOP = 'FOR_LOOP'
IMPORT_STATEMENT = 'IMPORT_STATEMENT'

PARENTHESIS = 'PARENTHESIS'  # common name
BRACES = 'BRACES'    # ()
FBRACES = 'FBRACES'  # {}
QBRACES = 'QBRACES'  # []

NEWLINE = characters['\n']
DOT = characters['.']
COMMA = characters[',']
COLON = characters[':']
SEMICOLON = characters[';']
EQUALS = characters['=']
EQEQUALS = characters['==']
IS = characters['===']
NOTIS = characters['!==']
PLUS = characters['+']
MINUS = characters['-']
SLASH = characters['/']
STAR = characters['*']
DOUBLESTAR = characters['**']
ANY = 'ANY'
