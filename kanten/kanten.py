import cv2
import numpy as np


def processImage(frame):
    """
    Process the provided image (3-channel BGR) and calculate
    gradients in X and Y direction as well as the gradient magnitude.

    gx and gy shall contain the gradient direction image with values between -1 and +1
    grad shall contain the gradient magnitude image with values between 0 and 1

    :param frame: 3-channel BGR image (np.array)
    :return: 3-tupel (gx, gy, grad) containing the gradient image in X and Y direction as well as the gradient magnitude image (1-channel np.float32 images each).
    """
    pass


def displayImage(gx, gy, grad):
    """
    Apply appropriate scaling and display the provided images.

    :param gx: Gradient image in X-Direction (np.float32 image with values between -1 and +1)
    :param gy: Gradient image in Y-Direction (np.float32 image with values between -1 and +1)
    :param grad: Gradient magnitude image (np.float32 image with values between 0 and 1)
    """
    pass


def mainLoop():
    """
    The main loop of this program
    """
    # TODO: Open the default camera

    while True:
        # TODO: Read next image from camera

        # TODO: Call processImage to retrieve properly scaled gradient direction and magnitude images

        # TODO: Call displayImage to display the images

        # TODO: Also display the original camera image in color

        # TODO: Break the infinite loop when the users presses ESCAPE (27)
        pass

    # TODO: Release the capture and writer objects


if __name__ == "__main__":
    mainLoop()
