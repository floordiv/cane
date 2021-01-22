from core.lex.lexer import Lexer
from core.semantic.parser import parse
from core.transpiler.python.code import generate


code = """
func my_func() {
    print('lol')
    return 5+5
}

if (5 == 5) {
    print('5 is 5')
} else {
    print('wait, what?')
}

response = my_func()
print(response)
"""

lexer = Lexer(code)
lexemes = lexer.parse()
final = parse(lexemes)
print(generate(final))
