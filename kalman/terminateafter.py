from SignalHub import Module, EngineMode, get_nested_key


class TerminateAfter(Module):
    def __init__(self):
        super().__init__(name="Terminate After", inputSignals=["config"])
        self.count = 0
        pass

    def start(self, data):
        self.counter = get_nested_key("config.simulation.steps", data, 120)
        self.count = 0
        return {}

    def step(self, data):
        self.count += 1
        if self.count >= self.counter:
            return {}, EngineMode.TERMINATE

        return {}

    def stop(self, data):
        pass
