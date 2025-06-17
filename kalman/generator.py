from SignalHub import Module, get_nested_key
import numpy as np

RANGE_X = (-50.0, 50.0)
RANGE_Y = (-50.0, 50.0)


class MeasurementGenerator(Module):
    def __init__(self):
        super().__init__(
            inputSignals=["config"],
            outputSchema={
                "type": "object",
                "properties": {
                    "measurements": {"type": "object", "properties": {}},
                    "groundtruth": {
                        "type": "object",
                        "properties": {
                            "state": {},
                        },
                        "additionalProperties": False,
                    },
                },
            },
        )

    def start(self, data):
        minDistance = get_nested_key("config.target.minDistance", data, 35.0)
        maxDistance = get_nested_key("config.target.maxDistance", data, 45.0)
        minVelocity = get_nested_key("config.target.minVelocity", data, 15.0)
        maxVelocity = get_nested_key("config.target.maxVelocity", data, 25.0)
        minAcceleration = get_nested_key("config.target.minAcceleration", data, 1.0)
        maxAcceleration = get_nested_key("config.target.maxAcceleration", data, 1.5)
        print(minDistance, maxDistance)

        sensors = data["config"]["sensors"]
        self.sensorOutageTimer = {}

        for sensor in sensors:
            name = sensor["name"]
            self.sensorOutageTimer[name] = 0

        gtX = np.random.uniform(RANGE_X[0], RANGE_X[1])
        gtY = np.random.uniform(RANGE_Y[0], RANGE_Y[1])
        self.position = np.array([gtX, gtY])
        self.position /= np.linalg.norm(self.position)
        self.position *= np.random.uniform(minDistance, maxDistance)

        gtX, gtY = self.position[0], self.position[1]
        vX = -gtX * np.random.uniform(0.8, 1.2)
        vY = -gtY * np.random.uniform(0.8, 1.2)
        self.velocity = np.array([vX, vY])
        self.velocity /= np.linalg.norm(self.velocity)
        self.velocity *= np.random.uniform(minVelocity, maxVelocity)

        velocityNorm = np.linalg.norm(self.velocity)
        if velocityNorm > 1e-2:
            self.acceleration = np.array([-gtY, -gtX])
            self.acceleration /= np.linalg.norm(self.velocity)
            self.acceleration *= np.random.uniform(minAcceleration, maxAcceleration)
        else:
            self.acceleration = np.array([0.0, 0.0])

        print(self.acceleration)

        self.steps = 0
        self.miss_timer = 0

        return {}

    def generate_missing_detections(self, sensor, measurement, covariance):
        # Get sensor miss chance and streak length
        missChance, missLength = (
            get_nested_key("missChance", sensor) or 0.1,
            get_nested_key("missLength", sensor) or 10,
        )

        # Miss out certain detections
        if self.steps > 3:
            sensorName = sensor["name"]
            if (
                self.sensorOutageTimer[sensorName] == 0
                and np.random.uniform() < missChance
            ):
                self.sensorOutageTimer[sensorName] = missLength

            if self.sensorOutageTimer[sensorName] > 0:
                measurement = None
                covariance = None
                self.sensorOutageTimer[sensorName] -= 1

        return measurement, covariance

    def generate_radar_measurement(self, sensor):
        # Get sensor position
        position = sensor["position"]
        position = np.array([position[0], position[1]])

        # Get sensor longitudinal and lateral uncertainty
        long, lat = sensor["longitudinalStdDev"], sensor["lateralStdDev"]

        # Get vector to target
        toTarget = self.position - position
        toTarget /= np.linalg.norm(toTarget)

        # Get rotation angle with position x axis
        alpha = np.arccos(-toTarget[0])

        s, c = np.sin(alpha), np.cos(alpha)
        R = np.array([[c, -s], [s, c]])

        covariance = R.T @ np.array([[long, 0], [0, lat]]) @ R

        measurement = np.random.multivariate_normal(self.position, covariance)

        return self.generate_missing_detections(sensor, measurement, covariance)

    def generate_global_measurement(self, sensor):
        # Get sensor position

        # Get sensor longitudinal and lateral uncertainty
        stdX, stdY, correlation = sensor["stdX"], sensor["stdY"], sensor["correlation"]

        # Get vector to target
        covariance = np.array(
            [
                [stdX**2, correlation * stdX * stdY],
                [correlation * stdX * stdY, stdY**2],
            ]
        )

        measurement = np.random.multivariate_normal(self.position, covariance)

        return self.generate_missing_detections(sensor, measurement, covariance)

    def step(self, data):
        scansPerSecond = get_nested_key("config.simulation.scansPerSecond", data, 33)
        # Move object
        self.position += self.velocity / scansPerSecond
        self.velocity += self.acceleration / scansPerSecond

        sensors = data["config"]["sensors"]
        measurements = {}
        for sensor in sensors:
            if sensor["type"] == "radar":
                measurement, covariance = self.generate_radar_measurement(sensor)
            elif sensor["type"] == "global":
                measurement, covariance = self.generate_global_measurement(sensor)

            name = sensor["name"]
            measurements[name] = {"state": measurement.reshape(-1,1), "covariance": covariance}

        self.steps += 1

        return {
            "groundtruth": {"state": self.position.copy()},
            "measurements": measurements,
        }

    def stop(self, data):
        pass
