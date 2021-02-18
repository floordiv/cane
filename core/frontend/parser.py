from core.lex.lexer import Lexer
from core.semantic.parser import parse as parse_semantic


def parse(raw_code):
    lexer = Lexer()
    lexemes = lexer.parse(raw_code)

    return parse_semantic(lexemes)
