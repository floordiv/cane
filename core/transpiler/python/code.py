class Generator:
    def __init__(self, code):
        self.code = code

    def generate_py_code(self):
        ...


def generate(code):
    generator = Generator(code)

    return generator.generate_py_code()
