import cv2
import numpy as np
from scipy import signal

def processImage(frame):
    # Turn image into float32 
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = np.float32(frame / 255.0)

    # Calculate Gradient in X and Y, scale appropiately
    gx = cv2.Sobel(frame, cv2.CV_32F, 1, 0, ksize=3) / 4.0
    gy = cv2.Sobel(frame, cv2.CV_32F, 0, 1, ksize=3) / 4.0

    # Calculate Ix^2, IxIy and Iy^2 images
    Ix2, IxIy, Iy2 = gx ** 2, gx * gy, gy ** 2

    Ix2 = cv2.blur(Ix2, ksize=(5,5))
    Iy2 = cv2.blur(Iy2, ksize=(5,5))
    IxIy = cv2.blur(IxIy, ksize=(5,5))

    # Harris Corner Strength
    kappa = 0.04
    det = Ix2 * Iy2 - IxIy ** 2
    trace = Ix2 + Iy2
    strength = det - kappa *  trace**2
    
    strength = np.clip(strength, 0.0, 1.0)
    strength /= np.max(strength) 

    cv2.imshow("Harris Corner Strength", strength)


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