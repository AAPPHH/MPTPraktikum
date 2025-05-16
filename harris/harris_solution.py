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
    Ix2, IxIy, Iy2 = gx**2, gx * gy, gy**2

    # Apply Block filter for summation, divide by size of kernel for normalization
    N = 7
    Ix2 = signal.convolve2d(Ix2, np.ones((N, N))) / (N**2)
    Iy2 = signal.convolve2d(Iy2, np.ones((N, N))) / (N**2)
    IxIy = signal.convolve2d(IxIy, np.ones((N, N))) / (N**2)

    # Harris Corner Strength
    kappa = 0.04
    det = Ix2 * Iy2 - IxIy**2
    trace = Ix2 + Iy2
    strength = det - kappa * trace**2

    strength /= np.max(strength)

    corners = np.zeros_like(strength)
    corners[strength > 0.1] = 1.0

    cv2.imshow("Harris Corner Strength", strength)
    cv2.imshow("Harris Corners", corners)


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
