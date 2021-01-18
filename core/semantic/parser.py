from core.objects.classes import Token
from core.objects.types import NEWLINE, EXPR
from core.objects.tools import get_token_index
from core.semantic.models import models, match, parsers
from core.objects.classes import FunctionCall, VarAssign


READ_VALUE_UNTIL_NEWLINE = (VarAssign,)
ALSO_EXPRS = (FunctionCall,)


def startswith(tokens: list):
    for model_class, model_matchtokens in models.items():
        matched, original_tokens_len = match(tokens, model_matchtokens, ignore=(NEWLINE,))

        if matched:
            return model_class, matched, original_tokens_len

    return None, None, 0


def parse(lexemes):
    output = []
    temp_expr = []

    while lexemes:
        model_class, tokens, tokens_len = startswith(lexemes)

        if model_class is None:
            one_token = lexemes.pop(0)

            if one_token.type != NEWLINE:
                temp_expr.append(one_token)
            elif temp_expr:
                output.append(Token(EXPR, temp_expr[:]))
                temp_expr.clear()
        else:
            if temp_expr:
                output.append(Token(EXPR, temp_expr[:]))

            if model_class in READ_VALUE_UNTIL_NEWLINE:
                until_newline = get_token_index(lexemes, NEWLINE)
                lexemes_until_newline = lexemes[tokens_len:until_newline]
                tokens.extend(lexemes_until_newline)
                tokens_len += len(lexemes_until_newline)

            parser = parsers[model_class]
            parsed_token = parser(parse, tokens)

            if model_class in ALSO_EXPRS:
                if output and output[-1].type == EXPR:
                    output[-1].value.append(parsed_token)
                else:
                    output.append(Token(EXPR, [parsed_token]))
            else:
                output.append(parsed_token)

            if temp_expr:
                temp_expr.clear()

            lexemes = lexemes[tokens_len:]

    if temp_expr:
        output.append(Token(EXPR, temp_expr))

    return output
