from core.objects import (types, tools, classes,
                          characters, keywords)

braces_openers = {
    '(': ')',
    '[': ']',
    '{': '}',
}
braces_types = {
    ')': types.BRACES,
    ']': types.QBRACES,
    '}': types.FBRACES,
}


class Lexer:
    def __init__(self, raw=None, context=None):
        if context is None:
            context = {}

        self.raw = raw
        self.context = context

    @staticmethod
    def prepare_raw_source(source):
        prepared_raw = ''

        for line in source.splitlines():
            prepared_line = tools.remove_comment(line).rstrip()
            prepared_raw += prepared_line + '\n'

        return prepared_raw[:-1]

    def parse(self, code=None, context=None):
        if code is None:
            if self.raw is None:
                raise TypeError('no source to lex given')

            code = self.raw
        if context is None:
            context = self.context

        code = self.prepare_raw_source(code)
        output_classes = [classes.Token(types.NO_TYPE, '')]
        skip_iters = 0
        lineno = 1

        for index, letter in enumerate(code):
            if letter == '\n':
                lineno += 1

            if skip_iters:
                skip_iters -= 1
                continue

            if letter == '\n':
                self.append(output_classes, classes.Token(types.NEWLINE, '\n'))
                output_classes.append(classes.Token(types.NO_TYPE, ''))
            elif letter == ' ':
                if output_classes[-1].value in keywords.keywords:  # other way, just skip it
                    keyword = output_classes[-1].value
                    keyword_type = keywords.keywords[keyword]

                    output_classes[-1] = classes.Token(keyword_type, keyword)

                self.append(output_classes, classes.Token(types.NO_TYPE, ''))
                continue
            elif letter in characters.special_characters:
                if output_classes[-1].type == types.OPERATOR and output_classes[-1].value + letter in \
                        characters.characters:
                    output_classes[-1].value += letter
                else:
                    if letter == '.' and output_classes[-1].type != types.OPERATOR:
                        output_classes[-1].value += '.'
                        continue

                    self.append(output_classes, classes.Token(types.OPERATOR, letter,
                                                              primary_type=types.OPERATOR))
            else:
                if letter in tuple('\'"'):
                    string, skip_iters = self.get_string_ending(code[index:])
                    string = string[1:-1].replace("\\'", "'").replace('\\"', '"')
                    string_token = classes.Token(types.STRING, string)
                    self.append(output_classes, string_token)
                    continue

                if output_classes[-1].type == types.OPERATOR:
                    self.append(output_classes, classes.Token(types.NO_TYPE, ''))

                output_classes[-1].value += letter

        if output_classes[-1].value == '':
            output_classes.pop()

        self.provide_token_type(output_classes[-1])
        parsed_but_no_unary = self.parse_braces(context, output_classes)
        final = self.parse_unary(parsed_but_no_unary)

        return final

    def append(self, lst: list, item: any):
        if lst[-1].type == types.NO_TYPE and lst[-1].value == '':
            lst[-1] = item
        else:
            lst.append(item)

        if len(lst) > 1:
            self.provide_token_type(lst[-2])

    def parse_unary(self, classes_):
        output_classes = []
        temp_signs = []

        for token in classes_:
            if token.primary_type == types.PARENTHESIS:
                token.value = self.parse_unary(token.value)

            if token.primary_type == types.OPERATOR and (
                    not output_classes or output_classes[-1].primary_type == types.OPERATOR):
                temp_signs.append(token)
            else:
                if temp_signs:
                    output_classes.append(self.get_unary_token(token, temp_signs))
                    temp_signs.clear()
                    continue

                output_classes.append(token)

        return output_classes + temp_signs

    def get_unary_token(self, token, signs):
        reversed_signs = signs[::-1]
        final_sign = reversed_signs[0].value

        for sign in reversed_signs[1:]:
            if sign.value == '-' and final_sign == '-':
                final_sign = '+'
            elif sign.value == '+' and final_sign == '-':
                final_sign = '-'
            else:
                final_sign = sign.value

        token.unary = final_sign

        if token.type in (types.INTEGER, types.FLOAT):
            self.apply_unary(token)

        return token

    @staticmethod
    def apply_unary(token):
        if token.unary == '-':
            token.value = -token.value
        elif token.unary == '+':
            token.value = +token.value

    @staticmethod
    def get_string_ending(string):
        opener = string[0]

        for index, letter in enumerate(string[1:], start=1):
            if letter == opener and string[index - 1] != '\\':
                return string[:index + 1], index

        return string, -1

    @staticmethod
    def provide_token_type(token):
        if token.type not in (types.OPERATOR, types.NO_TYPE):
            return

        if token.value.isdigit():
            token.type = token.primary_type = types.INTEGER
            token.value = int(token.value)
        elif tools.isfloat(token.value):
            token.type = token.primary_type = types.FLOAT
            token.value = float(token.value)
        elif token.type == types.NO_TYPE:
            if token.value in keywords.keywords:
                token.type = token.primary_type = keywords.keywords[token.value]
            else:
                token.type = token.primary_type = types.VARIABLE
        elif token.primary_type == types.OPERATOR:
            token.type = characters.characters[token.value]

    def parse_braces(self, context, classes_):
        opener = None
        opened = 0
        temp = []
        output = []

        for token in classes_:
            if token.value in braces_openers:
                if opener is None:
                    opener = token.value
                elif token.value == opener:
                    opened += 1
                    temp.append(token)
                else:
                    temp.append(token)
            elif opener and token.primary_type == types.OPERATOR and token.value == braces_openers[opener]:
                if opened:
                    opened -= 1
                    temp.append(token)
                else:
                    braces_type = braces_types[token.value]
                    new_token = classes.Token(braces_type, self.parse_braces(context, temp),
                                              primary_type=types.PARENTHESIS)

                    output.append(new_token)

                    temp.clear()
                    opener = None
                    opened = 0
            elif opener is not None:
                temp.append(token)
            else:
                output.append(token)

        if temp:
            raise SyntaxError('unclosed braces')

        return output


# lexer = Lexer('(1, 2, 2+1)')
# lexemes = lexer.parse()
# print(lexemes)
