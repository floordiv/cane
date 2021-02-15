class ExecuteCode:
    """
    Used in interpreter.logic. If function returned
    this class, executor will execute code from this
    class recursively
    """

    def __init__(self, code):
        self.code = code
