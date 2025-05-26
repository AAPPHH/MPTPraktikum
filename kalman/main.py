import numpy as np

from SignalHub import (
    Engine,
    Module,
    EngineMode,
    GALY,
    get_nested_key,
    ConfigParser,
    Webcam,
    Recorder,
    Replay,
)
import numpy as np
import argparse
import cv2


RANGE_X = (-50.0, 50.0)
RANGE_Y = (-50.0, 50.0)
SCANS_PER_SECOND = 33
CANVAS_WIDTH, CANVAS_HEIGHT = 1600, 1600

class TerminateAfter(Module):
    def __init__(self, count):
        super().__init__(name="Terminate After")
        self.counter = count
        self.count = 0
        pass

    def start(self, data):
        self.count = 0
        return {}

    def step(self, data):
        self.count += 1
        if self.count >= self.counter:
            return {}, EngineMode.TERMINATE

        return {}

    def stop(self, data):
        pass


class MeasurementGenerator(Module):
    def __init__(self):
        super().__init__(
            outputSchema={"type": "object", "properties": {
                "measurement": { 
                    "type": "object", 
                    "properties": {
                      "state": { },
                      "covariance": { }
                    }, 
                    "additionalProperties": False 
                  },
                  "groundtruth": { 
                    "type": "object", 
                    "properties": {
                      "state": { },
                    }, 
                    "additionalProperties": False 
                  },
                }
              }
        )

    def start(self, data):
        gtX = np.random.uniform(RANGE_X[0], RANGE_X[1])
        gtY = np.random.uniform(RANGE_Y[0], RANGE_Y[1])
        self.position = np.array([gtX, gtY])
        self.position /= np.linalg.norm(self.position)
        self.position = np.power(np.abs(self.position), 0.5) * np.sign(self.position)
        self.position *= np.random.uniform(50.0, 50.0)


        vX = -gtX * np.random.uniform(0.8, 1.2)
        vY = -gtY * np.random.uniform(0.8, 1.2)
        self.velocity = np.array([vX, vY])
        self.velocity /= np.linalg.norm(self.velocity)
        self.velocity *= np.random.uniform(15.0, 25.0) 

        self.acceleration = np.array([-gtY, -gtX])
        self.acceleration /= np.linalg.norm(self.velocity)
        self.acceleration *= np.random.uniform(1.0, 1.5) 

        self.steps = 0
        self.miss_timer = 0

        return {}

    def step(self, data):
        # Move object
        self.position += self.velocity / SCANS_PER_SECOND
        self.velocity += self.acceleration / SCANS_PER_SECOND

        # Make a measurement   
        covariance = np.array([
            [1.0, 0.0],
            [0.0, 1.0]
        ])
        measurement = np.random.multivariate_normal(self.position, covariance)

        # Miss out certain detections
        if self.steps > 30:
            if self.miss_timer == 0 and np.random.uniform() < 0.1:
                self.miss_timer = 15
                
            if self.miss_timer > 0:
                measurement = None
                covariance = None
                self.miss_timer -= 1
        
        self.steps += 1

        return { 
            "groundtruth": {
                "state": self.position.copy()
            },
            "measurement": {
                "state": measurement,
                "covariance": covariance
            },
        }

    def stop(self, data):
        pass
    
class KalmanFilter(Module):
    def __init__(self):    
        super().__init__(inputSignals=["measurement"], outputSchema={
            "type": "object", "properties": {
                  "prior": { 
                    "type": "object", 
                    "properties": {
                      "state": { },
                      "covariance": { }
                    }, 
                    "additionalProperties": False 
                  },
                  "posterior": { 
                    "type": "object", 
                    "properties": {
                      "state": { },
                      "covariance": { }
                    }, 
                    "additionalProperties": False 
                  },
                }
              })

        self.X = None
        self.P = None
    
    def step(self, data):
        z = data["measurement"]["state"]
        if z is not None:
            z = z.reshape(-1,1)

        R = data["measurement"]["covariance"]

        if self.X is None:
            self.X = np.array([[z[0][0], z[1][0], 0.0, 0.0]]).T
            self.P = np.array([
                [R[0][0], 0.0, 0.0, 0.0],
                [0.0, R[1][1], 0.0, 0.0],
                [0.0, 0.0, 100.0, 0.0],
                [0.0, 0.0, 0.0, 100.0],
                ])
            
            prediction = self.X.copy()
            priorCov = self.P.copy()
        else:
            F = np.array([
                [1.0, 0.0, 1.0, 0.0],
                [0.0, 1.0, 0.0, 1.0],
                [0.0, 0.0, 1.0, 0.0],
                [0.0, 0.0, 0.0, 1.0],
                ]
                )
            
            Q = np.eye(4) * 0.001

            self.X = F @ self.X 
            self.P = F @ self.P @ F.T + Q
            
            prediction = self.X.copy()
            priorCov = self.P.copy()

            H = np.array([
                [1.0, 0.0, 0.0, 0.0],
                [0.0, 1.0, 0.0, 0.0]
            ])

            if z is not None:
              y = z - H @ self.X 
              S = H @ self.P @ H.T + R 
              K = self.P @ H.T @ np.linalg.inv(S)

              self.X = self.X + K @ y
              self.P = (np.eye(4) - K @ H) @ self.P

        return {
            "prior": {
                "state": prediction,
                "covariance": priorCov
            },
            "posterior": {
                "state": self.X,
                "covariance": self.P
            }
        }
  


class Visualization(Module):
    def __init__(self):
        super().__init__(inputSignals=["measurement", "groundtruth", "prior", "posterior"])
        self.measurement_state_history = []
        self.gt_state_history = []
        self.prior_state_history = []
        self.posterior_state_history = []

    def layer(self, name, galy):
        galy.layer(name)

        # Setup affine mapping to image
        scaleX = CANVAS_WIDTH / (RANGE_X[1] - RANGE_X[0])
        scaleY = CANVAS_HEIGHT / (RANGE_Y[0] - RANGE_Y[1])
        translateX = -RANGE_X[0] * scaleX
        translateY = -RANGE_Y[1] * scaleY

        mapping = np.array([
            [scaleX, 0.0, translateX],
            [0.0, scaleY, translateY]
            ])
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
        galy.mahalanobis(state, cov, base_color + 0.33 * (white - base_color), scale=2.0, thickness=2)
        galy.mahalanobis(state, cov, base_color + 0.67 * (white - base_color), scale=3.0, thickness=2)

    def step(self, data):
        # Append states to history
        measurement = data["measurement"]["state"]
        if measurement is not None:
          self.measurement_state_history.append(data["measurement"]["state"])

        self.gt_state_history.append(data["groundtruth"]["state"])
        self.prior_state_history.append(data["prior"]["state"][:2, 0])
        self.posterior_state_history.append(data["posterior"]["state"][:2, 0])

        # Draw GALY
        galy = GALY()
        galy.canvas("Main", (CANVAS_WIDTH, CANVAS_HEIGHT), (1.0, 1.0, 1.0))
        self.layer("Grid", galy)
       
        # Draw coordinate grid
        for x in [-50.0, -40.0, -30.0, -20.0, -10.0, 0.0, 10.0, 20.0, 30.0, 40.0]:
            galy.line((x, -50.0), (x, 50.0), (0.8, 0.8, 0.8), 1)

            galy.putText(f"{x:.0f}", (x + 1.0, 2.0), fontScale=0.4, color=(0.5, 0.5, 0.5))
            galy.putText(f"{x:.0f}", (1.0, x + 2.0), fontScale=0.4, color=(0.5, 0.5, 0.5))

            galy.line((-50.0, x), (50.0, x), (0.8, 0.8, 0.8), 1)

        galy.line((0.0, -50.0), (0.0, 50.0), (0.0, 0.0, 0.0), 2)
        galy.line((-50.0, 0.0), (50.0, 0.0), (0.0, 0.0, 0.0), 2)

        
        # Draw ground truth state
        self.draw_state_history(layerName = "Ground Truth", galy = galy, history = self.gt_state_history, base_color = np.array([0.2, 0.2, 1.0]), white = np.array([0.7, 0.7, 1.0]))
        
        # Draw detection history
        self.draw_state_history(layerName = "Measurement History", galy = galy, history = self.measurement_state_history, base_color = np.array([1.0, 0.2, 0.2]), white = np.array([1.0, 0.7, 0.7]))

        # Draw detection
        if measurement is not None:
          self.draw_state("Measurement", galy, data["measurement"]["state"], data["measurement"]["covariance"], np.array([1.0, 0.2, 0.2]))
        else:
          galy.putText("Measurement missing", (-49,48), color=(0.2, 0.0, 0.9), thickness=2)

        # Draw prior history
        self.draw_state_history(layerName = "Prior History", galy = galy, history = self.prior_state_history, base_color = np.array([0.2, 0.5, 0.2]), white = np.array([0.7, 1.0, 0.7]))

        # Draw prior
        state = data["prior"]["state"][:2, 0]
        cov = data["prior"]["covariance"][:2, :2]
        self.draw_state("Prior", galy, state, cov, np.array([0.2, 0.5, 0.2]))

        # Draw posterior history
        self.draw_state_history(layerName = "Posterior History", galy = galy, history = self.posterior_state_history, base_color = np.array([0.1, 0.2, 0.1]), white = np.array([0.3, 0.5, 0.3]))

        # Draw prior
        state = data["posterior"]["state"][:2, 0]
        cov = data["posterior"]["covariance"][:2, :2]
        self.draw_state("Posterior", galy, state, cov, np.array([0.1, 0.2, 0.1]))

        

        return { "galy": galy }
        

class Clock(Module):
    def __init__(self):
        super().__init__(outputSchema={"type": "object", "properties": { "A" : {} }})

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
        return {"clock": galy, "A": 3 }

    def stop(self, data):
        pass


parser = argparse.ArgumentParser("Example Program")
parser.add_argument("--mode", action="store", default="none")
parser.add_argument("--recorder.file", action="store")
parser.add_argument("--engine.singlestep", action="store_true", default=False)
parser.add_argument("--webcam.width", required=False)
modules = [ConfigParser(parser), MeasurementGenerator(), KalmanFilter(), Visualization(), TerminateAfter(120)]


engine = Engine(modules=modules, signals={})
signals = engine.run({})
