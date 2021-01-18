from core.lex.lexer import Lexer
from core.semantic.parser import parse


code = """
func my_func() {
    return 5
}

response = my_func()
print(response)
"""

lexer = Lexer(code)
lexemes = lexer.parse()
final = parse(lexemes)
print(final)
