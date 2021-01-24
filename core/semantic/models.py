from core.objects.types import (BRACES, FBRACES, QBRACES,
                                VARIABLE, EQUALS, ANY)
from core.objects.classes import (MatchToken, FunctionCall, Function,
                                  VarAssign, ReturnStatement, IfBranchLeaf,
                                  ElifBranchLeaf, ElseBranchLeaf)
from core.semantic.parsers import (var_assign, function, function_call,
                                   return_statement, if_branch, elif_branch,
                                   else_branch)
from core.objects.keywords import (FUNCASSIGN_KEYWORD, RETURN_KEYWORD, IF_KEYWORD,
                                   ELIF_KEYWORD, ELSE_KEYWORD)


models = {
    VarAssign: (MatchToken(VARIABLE), MatchToken(EQUALS), MatchToken(ANY)),
    Function: (MatchToken(FUNCASSIGN_KEYWORD), MatchToken(VARIABLE), MatchToken(BRACES), MatchToken(FBRACES)),
    FunctionCall: (MatchToken(VARIABLE), MatchToken(BRACES)),
    ReturnStatement: (MatchToken(RETURN_KEYWORD), MatchToken(ANY)),
    IfBranchLeaf: (MatchToken(IF_KEYWORD), MatchToken(BRACES), MatchToken(FBRACES)),
    ElifBranchLeaf: (MatchToken(ELIF_KEYWORD), MatchToken(BRACES), MatchToken(FBRACES)),
    ElseBranchLeaf: (MatchToken(ELSE_KEYWORD), MatchToken(FBRACES)),
}
parsers = {
    VarAssign: var_assign,
    Function: function,
    FunctionCall: function_call,
    ReturnStatement: return_statement,
    IfBranchLeaf: if_branch,
    ElifBranchLeaf: elif_branch,
    ElseBranchLeaf: else_branch,
}


def match(original, match_list, ignore=()):
    if len(original) > len(match_list):
        original = original[:len(match_list)]

    current_match_token_index = 0
    matched = []

    for token in original:
        if token.type in ignore or token.primary_type in ignore:
            continue

        if not match_list[current_match_token_index].match(token):
            return False, 0

        matched.append(token)
        current_match_token_index += 1

    if len(matched) != len(match_list):
        """
        if output tokens counter does not equals match list length, it means, that
        match_list does not matches given array of tokens
        """
        return False, 0

    return matched, len(original)
