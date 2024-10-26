class Runtime:
    def __init__(self, parent):
        self.parent = parent

    def read_register(self, module, register):
        register_runtime = self.parent.hvi_handle.sync_sequence.scopes[
            module
        ].registers[register]
        value = register_runtime.read()
        return value

    def write_register(self, module, register, value):
        register_runtime = self.parent.hvi_handle.sync_sequence.scopes[
            module
        ].registers[register]
        register_runtime.write(value)
        return value
