from SignalHub import Module, GALY
import numpy as np


class Clock(Module):
    def __init__(self):
        super().__init__(outputSchema={"type": "object", "properties": {"A": {}}})

    def start(self, data):
        self.counter = 0
        return {}

    def step(self, data):
        galy = GALY()

        galy.canvas("Clock", (640, 480), (0.0, 0.0, 0.0))

        rad = -np.pi / 2.0 + 5.0 * self.counter / 99.0 * np.pi * 2.0
        x0, x1 = 320, int(320.0 + 160.0 * np.cos(rad))
        y0, y1 = 240, int(240.0 + 160.0 * np.sin(rad))
        galy.layer("Minute Hand")
        galy.line((x0, y0), (x1, y1), (1.0, 0.0, 0.0), 2)

        rad2 = -np.pi / 2.0 + self.counter / 99.0 * np.pi * 2.0
        x0, x1 = 320, int(320.0 + 80.0 * np.cos(rad2))
        y0, y1 = 240, int(240.0 + 80.0 * np.sin(rad2))

        galy.layer("Hour Hand")
        galy.line((x0, y0), (x1, y1), (1.0, 0.0, 0.0), 2)

        self.counter += 1
        return {"clock": galy, "A": 3}

    def stop(self, data):
        pass
