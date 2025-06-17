from generator import RANGE_X, RANGE_Y
from SignalHub import Module, GALY
import numpy as np

CANVAS_WIDTH, CANVAS_HEIGHT = 1280, 1280


class Visualization(Module):
    def __init__(self):
        super().__init__(
            inputSignals=["config", "measurements", "groundtruth", "prior", "posterior"]
        )
        self.measurement_state_history = {}
        self.gt_state_history = []
        self.prior_state_history = []
        self.posterior_state_history = []

    def start(self, data):
        # Create a dedicated measurement state history for each measurement
        sensors = data["config"]["sensors"]
        for sensor in sensors:
            name = sensor["name"]
            self.measurement_state_history[name] = []

        return {}

    def layer(self, name, galy, alwaysVisible=False):
        galy.layer(name, alwaysVisible)

        # Setup affine mapping to image
        scaleX = CANVAS_WIDTH / (RANGE_X[1] - RANGE_X[0])
        scaleY = CANVAS_HEIGHT / (RANGE_Y[0] - RANGE_Y[1])
        translateX = -RANGE_X[0] * scaleX
        translateY = -RANGE_Y[1] * scaleY

        mapping = np.array([[scaleX, 0.0, translateX], [0.0, scaleY, translateY]])
        galy.set_layer_affine_mapping(mapping)

    def draw_state_history(self, layerName, galy, history, base_color, white):
        self.layer(layerName, galy)
        prev_state = None

        alpha = 1.0
        for state in reversed(history):
            color = base_color * alpha + white * (1.0 - alpha)
            alpha *= 0.96

            if prev_state is not None:
                galy.line(prev_state, state, (color[0], color[1], color[2]))
                pass

            galy.circle(state, 5, (color[0], color[1], color[2]), -1)

            prev_state = state

    def draw_state(self, layerName, galy, state, cov, base_color):
        self.layer(layerName, galy)

        white = np.array([1.0, 1.0, 1.0])

        galy.mahalanobis(state, cov, base_color, scale=1.0, thickness=2)
        galy.mahalanobis(
            state, cov, base_color + 0.33 * (white - base_color), scale=2.0, thickness=2
        )
        galy.mahalanobis(
            state, cov, base_color + 0.67 * (white - base_color), scale=3.0, thickness=2
        )

    def draw_sensor(self, galy, sensor):
        if sensor["type"] == "radar":
            position = sensor["position"]
            for radius in [3, 7, 11]:
                col = 0.1 + radius * 0.03
                galy.circle(position, radius, (col, col, col), 2)

            x = position[0] - 2.2
            y = position[1] - 2.5
            galy.putText(
                sensor["name"],
                (x, y),
                color=(0.1, 0.1, 0.1),
                fontScale=0.6,
                thickness=1,
            )

    def step(self, data):
        # Append states to history
        for sensorName, measurement in data["measurements"].items():
            state = measurement["state"]
            if state is not None:
                self.measurement_state_history[sensorName].append(state)

        self.gt_state_history.append(data["groundtruth"]["state"])
        self.prior_state_history.append(data["prior"]["state"][:2, 0])
        self.posterior_state_history.append(data["posterior"]["state"][:2, 0])

        # Draw GALY
        galy = GALY()
        galy.canvas("Main", (CANVAS_WIDTH, CANVAS_HEIGHT), (1.0, 1.0, 1.0))

        # Draw sensor configuration
        self.layer("Sensors", galy)
        sensors = data["config"]["sensors"]
        for sensor in sensors:
            self.draw_sensor(galy, sensor)

        self.layer("Grid", galy, alwaysVisible=True)

        # Draw coordinate grid
        for x in [-50.0, -40.0, -30.0, -20.0, -10.0, 0.0, 10.0, 20.0, 30.0, 40.0]:
            galy.line((x, -50.0), (x, 50.0), (0.8, 0.8, 0.8), 1)

            galy.putText(
                f"{x:.0f}", (x + 1.0, 2.0), fontScale=0.4, color=(0.5, 0.5, 0.5)
            )
            galy.putText(
                f"{x:.0f}", (1.0, x + 2.0), fontScale=0.4, color=(0.5, 0.5, 0.5)
            )

            galy.line((-50.0, x), (50.0, x), (0.8, 0.8, 0.8), 1)

        galy.line((0.0, -50.0), (0.0, 50.0), (0.0, 0.0, 0.0), 2)
        galy.line((-50.0, 0.0), (50.0, 0.0), (0.0, 0.0, 0.0), 2)

        # Draw ground truth state
        self.draw_state_history(
            layerName="Ground Truth",
            galy=galy,
            history=self.gt_state_history,
            base_color=np.array([0.2, 0.2, 1.0]),
            white=np.array([0.7, 0.7, 1.0]),
        )

        # Draw detection history
        for sensorName, history in self.measurement_state_history.items():
            self.draw_state_history(
                layerName=f"Measurement History - {sensorName}",
                galy=galy,
                history=history,
                base_color=np.array([1.0, 0.2, 0.2]),
                white=np.array([1.0, 0.7, 0.7]),
            )

        # Draw detection
        for sensorName, measurement in data["measurements"].items():
            state = measurement["state"]
            covariance = measurement["covariance"]
            if state is not None:
                self.draw_state(
                    f"Measurement - {sensorName}",
                    galy,
                    state,
                    covariance,
                    np.array([1.0, 0.2, 0.2]),
                )
            else:
                galy.putText(
                    "Measurement missing", (-49, 48), color=(0.2, 0.0, 0.9), thickness=2
                )

        # Draw prior history
        self.draw_state_history(
            layerName="Prior History",
            galy=galy,
            history=self.prior_state_history,
            base_color=np.array([0.2, 0.5, 0.2]),
            white=np.array([0.7, 1.0, 0.7]),
        )

        # Draw prior
        state = data["prior"]["state"][:2, 0]
        cov = data["prior"]["covariance"][:2, :2]
        self.draw_state("Prior", galy, state, cov, np.array([0.2, 0.5, 0.2]))

        # Draw posterior history
        self.draw_state_history(
            layerName="Posterior History",
            galy=galy,
            history=self.posterior_state_history,
            base_color=np.array([0.1, 0.2, 0.1]),
            white=np.array([0.3, 0.5, 0.3]),
        )

        # Draw prior
        state = data["posterior"]["state"][:2, 0]
        cov = data["posterior"]["covariance"][:2, :2]
        self.draw_state("Posterior", galy, state, cov, np.array([0.1, 0.2, 0.1]))

        return {"galy": galy}
