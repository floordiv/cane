def encode(string, encoding='utf-8'):
    return string.encode(encoding)


def decode(string, encoding='utf-8'):
    return string.decode(encoding)


__version__ = (0, 0, 1)


binds = {
    'print': print,
    'input': input,
    'true': True,
    'false': False,
    'null': None,
    'encode': encode,
    'decode': decode,
    '__version__': __version__
}
