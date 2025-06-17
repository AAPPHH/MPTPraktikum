import numpy as np
import argparse
from SignalHub import Engine, Module, ConfigParser
from generator import MeasurementGenerator
from visualization import Visualization
from terminateafter import TerminateAfter

class KalmanFilter(Module):
    def __init__(self):
        super().__init__(
            inputSignals=["measurements"],
            outputSchema={
                "type": "object",
                "properties": {
                    "prior": {
                        "type": "object",
                        "properties": {"state": {}, "covariance": {}},
                        "additionalProperties": False,
                    },
                    "posterior": {
                        "type": "object",
                        "properties": {"state": {}, "covariance": {}},
                        "additionalProperties": False,
                    },
                },
            },
        )

        self.X, self.P = None, None
        self.prediction, self.priorCov = None, None

    def predict(self):
        """
        Predicts the next state and covariance of the system using the Kalman filter prediction step.
        This method applies the state transition model to estimate the next state vector (`self.X`)
        and updates the state covariance matrix (`self.P`) by incorporating process noise.
        The prediction is based on the following:
          - State transition matrix (F) models the system dynamics.
          - Process noise covariance matrix (Q) accounts for uncertainty in the process.

        For a 2D position and velocity model, the state vector is represented as:
        [x_position, y_position, x_velocity, y_velocity]. The state transition matrix F 
        is designed to update the position based on the current velocity, assuming a constant
        velocity model. The process noise covariance matrix Q is set to a small value to reflect
        the uncertainty in the process.  

        Assuming constant velocity, the state transition matrix F is defined as:

            F = [[1, 0, dt, 0],
                [0, 1, 0, dt],
                [0, 0, 1, 0],
                [0, 0, 0, 1]]

        where dt is the time step between predictions. In this case, we assume dt = 1 for simplicity.

        The process noise covariance matrix Q is defined as:  

            Q = [[q_x, 0, 0, 0],
                [0, q_y, 0, 0],
                [0, 0, q_vx, 0],
                [0, 0, 0, q_vy]]

        where q_x, q_y, q_vx, and q_vy are small values representing the process noise for position. 

        Use np.diag to create a diagonal matrix for Q, where the diagonal elements represent the process noise variances for each state variable.^
        Use small noise for position and larger noise for velocity to reflect the uncertainty in the process.
        The prediction step updates the state vector and covariance matrix as follows:  
        
        - `X = F @ X`: This updates the state vector by applying the state transition matrix F.
        - `P = F @ P @ F.T + Q`: This updates the state covariance matrix by applying the state transition matrix F, its transpose, and adding the process noise covariance matrix Q.
        
        Updates:
          self.X: Predicted state vector after applying the state transition.
          self.P: Predicted state covariance matrix after accounting for process noise.
        """
        
        # TODO: Define the state transition matrix F
        F = np.array(
            [
                [1.0, 0.0, 1.0, 0.0],
                [0.0, 1.0, 0.0, 1.0],
                [0.0, 0.0, 1.0, 0.0],
                [0.0, 0.0, 0.0, 1.0],
            ]
        )

        # TODO: Define the process noise covariance matrix Q
        Q = np.diag([0.001, 0.001, 0.1, 0.1])

        # TODO: Predict next state using the state transition matrix
        self.X = F @ self.X

        # TODO: Update the state covariance matrix using the state transition matrix and process noise
        self.P = F @ self.P @ F.T + Q

    def init_filter(self, z, R):
        """
        Initializes the Kalman filter with thje first measurement and covariance.
        
        Parameters:
        - z: The first measurement (2D Vector with position in X and Y).
        - R: The covariance matrix associated with the measurement, which represents the uncertainty in the measurement.
        
        This method sets the initial state and covariance for the Kalman filter, which will be used
        in subsequent prediction and update steps.

        The state vector `self.X` is initialized with the first measurement, assuming a 2D position and velocity model.
        The covariance matrix `self.P` is initialized with the measurement noise covariance `R` for position, 
        and larger values for velocity to reflect the uncertainty in the initial state.
        
        Updates:
          self.X: Predicted state vector after applying the state transition.
          self.P: Predicted state covariance matrix after accounting for process noise.
        """
        # TODO: Initialize the state vector with the initial measurement, assuming a 2D position and velocity model. 
        # Use the X and Y component of the measurement z, and set the velocity components to 0.0.
        # HINT: The resulting state vector should be a 4D vector with the format [x_position, y_position, x_velocity, y_velocity] with shape (4, 1).
        self.X = np.array([[z[0][0], z[1][0], 0.0, 0.0]]).T

        # TODO: Initialize the covariance matrix with the measurement noise covariance R for position,
        # and larger values for velocity to reflect the uncertainty in the initial state. 
        # HINT: The resulting covariance matrix should be a 4x4 matrix. You can use np.diag to create a diagonal matrix.        
        self.P = np.diag([R[0][0], R[1][1], 100.0, 100.0])


    def update(self, z, R):
        """
        Performs the Kalman filter update step with the given measurement.
        Args:
          z (np.ndarray): The measurement vector. Shape is (2,1) for 2D position (no velocity estimates from the measurement).
          R (np.ndarray): The measurement noise covariance matrix. Shape is (2,2) for 2D position measurements.
        Updates:
          self.X (np.ndarray): The state estimate after incorporating the measurement.
          self.P (np.ndarray): The state covariance matrix after the update.

        If the filter is not initialized (self.X is None), initializes the filter with the measurement.
        Otherwise, computes the Kalman gain, updates the state estimate and covariance matrix.

        First, one needs to calculate the innovation (measurement residual) `y` and the innovation covariance `S`:
        :math:`\begin{array}{ccc}
                y &=& z - H\cdot X\\
                S &=& H \cdot P \cdot H^T + R
               \end{array}`
        
        where `z` is the measurement, `H` is the measurement matrix, `X` is the current state estimate, and `P` is the current covariance matrix.

        Then, compute the Kalman gain `K`:
        :math:`K = P \cdot H^T \cdot S^{-1}`

        Finally, update the state estimate and covariance matrix:

        :math:`X = X + K  \cdot y`
        :math:`P = (I - K \cdot H) \cdot P`

        where `H` is the measurement matrix and `I` is the identity matrix
        """
        # TODO: If the filter is not initialized, initialize it with the first measurement and return
        if self.X is None:
            self.init_filter(z, R)
            return

        ### TODO: Define the measurement matrix H
        H = np.array([[1.0, 0.0, 0.0, 0.0], 
                      [0.0, 1.0, 0.0, 0.0]])

        ## TODO: Calculate the innovation (measurement residual) y and the innovation covariance S
        y = z - H @ self.X
        S = H @ self.P @ H.T + R

        ## TODO: Compute the Kalman gain K
        K = self.P @ H.T @ np.linalg.inv(S)

        # TODO: Update the state estimate with the measurement
        self.X = self.X + K @ y
        self.P = (np.eye(4) - K @ H) @ self.P

    def step(self, data):
        # If there is a state already, predict the next state and covariance
        # Also, make a copy of the current state and covariance for visualization of the prior 
        if self.X is not None:
            self.predict()
            self.prediction = self.X.copy()
            self.priorCov = self.P.copy()

        # We iterate over all measurements in the data and update the filter with each measurement.
        for _, measurement in data["measurements"].items():
            # Extract the measurement state and covariance
            z, R = measurement["state"], measurement["covariance"]

            # If there is an actual measurenent, update the filter with the measurement
            # Measurements may be missing, in which case z and R are None.
            if z is not None and R is not None: 
              self.update(z, R)

            # If the filter has not been initialized yet, we set the prediction and priorCov to the current state and covariance
            if self.prediction is None and self.priorCov is None:
                self.prediction = self.X.copy()
                self.priorCov = self.P.copy()

        # Return the prior and posterior state and covariance
        return {
            "prior": {"state": self.prediction, "covariance": self.priorCov},
            "posterior": {"state": self.X, "covariance": self.P},
        }


################################################# 
# Main program to run the Kalman filter example #
# Donot modify the code below this line        #
#################################################

parser = argparse.ArgumentParser("Example Program")
parser.add_argument("--mode", action="store", default="none")
parser.add_argument("--recorder.file", action="store")
parser.add_argument("--engine.singlestep", action="store_true", default=False)
parser.add_argument("--webcam.width", required=False)
modules = [
    ConfigParser(parser),
    MeasurementGenerator(),
    KalmanFilter(),
    Visualization(),
    TerminateAfter(),
]

engine = Engine(modules=modules, signals={})
signals = engine.run({})
