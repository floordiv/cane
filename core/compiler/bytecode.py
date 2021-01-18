class Generator:
    def __init__(self, code):
        self.code = code

    def generate_llvm_asm(self):
        ...


def generate(code):
    generator = Generator(code)

    return generator.generate_llvm_asm()
