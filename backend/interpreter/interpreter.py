from typing import List

from lib.std import builtins
from core.objects import classes
from core.frontend.parser import parse
from backend.interpreter.scopes import Scope
from backend.interpreter.internal_tokens import original_tokens2internal, Token

DEDICATED_SCOPES_FOR_TOKENS = (
    classes.Function,
)


def interpret(raw: str):
    tokens = parse(raw)


def gen_scopes(tokens):
    current_scope = Scope(init_vars=builtins.binds)
    final_tokens: List[List[Token, Scope]] = []

    for token in tokens:
        if classof(token) in DEDICATED_SCOPES_FOR_TOKENS:
            final_tokens.append([token, Scope(init_vars=builtins.binds)])
        else:
            final_tokens.append([token, current_scope])

    return final_tokens


def token2internaltoken(scope, token):
    class_of_original_token = classof(token)
    internal_token_class = original_tokens2internal.get()

    if internal_token_class is None:
        raise NotImplemented(f'token {class_of_original_token} not supported')

    return internal_token_class(scope, token)


def classof(obj):
    return obj.__class__
