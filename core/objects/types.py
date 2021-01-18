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
EXPR = 'EXPR'   # function calls, math operations, etc.

PARENTHESIS = 'PARENTHESIS'  # common name
BRACES = 'BRACES'    # ()
FBRACES = 'FBRACES'  # {}
QBRACES = 'QBRACES'  # []

NEWLINE = characters['\n']
DOT = characters['.']
COMMA = characters[',']
COLON = characters[':']
EQUALS = characters['=']
ANY = 'ANY'
