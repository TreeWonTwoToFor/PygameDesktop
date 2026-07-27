class App:
    def __init__(self, id, name, icon, module, dropdown):
        self.id = id
        self.name = name
        self.icon = icon
        self.module = module
        self.dropdown = dropdown

        self.state = self.module.run_once()

    def run(self, desktop_window_dict, desktop_instruction):
        canvas = desktop_window_dict[self.id].surface
        output = self.module.run(self.id, self.state, canvas, desktop_instruction)
        if output is not None:
            self.state = output