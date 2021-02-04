from core.transpiler.python.builder import builders


def remove_useless_newlines(source):
    return source.strip('\n') + '\n'


def generate(code, indent=0):
    source = ''
    indentation = '    ' * indent

    for token in code:
        if token.type not in builders:
            raise Warning('Unsupported token: ' + str(token))

        py_source = builders[token.type](generate, token, indent=indent)
        justified_by_indentation = indentation + indentation.join(py_source.splitlines(keepends=True))
        source += justified_by_indentation

    return remove_useless_newlines(source)
