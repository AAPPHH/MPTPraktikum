from SignalHub import Module, EngineMode, get_nested_key


class TerminateAfter(Module):
    def __init__(self):
        super().__init__(name="Terminate After", inputSignals=["config"])
        self.count = 0
        pass

    def start(self, data):
        self.counter = int(get_nested_key("config.simulation.simulateSeconds", data, 2.0) * get_nested_key("config.simulation.scansPerSecond", data, 30.0))
        self.count = 0
        return {}

    def step(self, data):
        self.count += 1
        if self.count >= self.counter:
            return {}, EngineMode.TERMINATE

        return {}

    def stop(self, data):
        pass
