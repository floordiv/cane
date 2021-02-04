import core.objects.types as types
import core.objects.classes as classes
import core.objects.keywords as keywords
import core.semantic.parsers as tokens_parsers

from core.objects.classes import MatchToken


models = {
    classes.VarAssign: (MatchToken(types.VARIABLE), MatchToken(types.EQUALS), MatchToken(types.ANY)),
    classes.Function: (MatchToken(keywords.FUNCASSIGN_KEYWORD), MatchToken(types.VARIABLE), MatchToken(types.BRACES),
                       MatchToken(types.FBRACES)),
    classes.FunctionCall: (MatchToken(types.VARIABLE), MatchToken(types.BRACES)),
    classes.ReturnStatement: (MatchToken(keywords.RETURN_KEYWORD), MatchToken(types.ANY)),
    classes.IfBranchLeaf: (MatchToken(keywords.IF_KEYWORD), MatchToken(types.BRACES), MatchToken(types.FBRACES)),
    classes.ElifBranchLeaf: (MatchToken(keywords.ELIF_KEYWORD), MatchToken(types.BRACES), MatchToken(types.FBRACES)),
    classes.ElseBranchLeaf: (MatchToken(keywords.ELSE_KEYWORD), MatchToken(types.FBRACES)),
    classes.WhileLoop: (MatchToken(keywords.WHILE_LOOP_KEYWORD), MatchToken(types.BRACES), MatchToken(types.FBRACES)),
    classes.ForLoop: (MatchToken(keywords.FOR_LOOP_KEYWORD), MatchToken(types.BRACES), MatchToken(types.FBRACES)),
    classes.BreakStatement: (MatchToken(keywords.BREAK_KEYWORD),),
    classes.ContinueStatement: (MatchToken(keywords.CONTINUE_KEYWORD),),
    classes.ImportStatement: (MatchToken(keywords.IMPORT_KEYWORD), MatchToken(types.STRING),
                              MatchToken(keywords.AS_KEYWORD), MatchToken(types.VARIABLE)),
}
parsers = {
    classes.VarAssign: tokens_parsers.var_assign,
    classes.Function: tokens_parsers.function,
    classes.FunctionCall: tokens_parsers.function_call,
    classes.ReturnStatement: tokens_parsers.return_statement,
    classes.IfBranchLeaf: tokens_parsers.if_branch,
    classes.ElifBranchLeaf: tokens_parsers.elif_branch,
    classes.ElseBranchLeaf: tokens_parsers.else_branch,
    classes.WhileLoop: tokens_parsers.while_loop,
    classes.ForLoop: tokens_parsers.for_loop,
    classes.BreakStatement: tokens_parsers.break_statement,
    classes.ContinueStatement: tokens_parsers.continue_statement,
    classes.ImportStatement: tokens_parsers.import_statement,
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
