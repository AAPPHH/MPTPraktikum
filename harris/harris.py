import cv2
import numpy as np
from scipy import signal

def processImage(frame):
    # TODO: Implement according to instructions
    pass


def mainLoop():
    """
    The main loop of this program
    """
    # TODO: Open the default camera
    cam = cv2.VideoCapture(0)

    while True:
        # TODO: Read next image from camera
        _, frame = cam.read()

        # TODO: Call processImage to retrieve properly scaled gradient direction and magnitude images
        processImage(frame)

        # TODO: Also display the original camera image in color
        cv2.imshow("Camera", frame)

        # TODO: Break the infinite loop when the users presses ESCAPE (27)
        if cv2.waitKey(1) == 27:
            break

    # TODO: Release the capture and writer objects
    cam.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    mainLoop()