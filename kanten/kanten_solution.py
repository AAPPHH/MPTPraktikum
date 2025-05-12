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
    # TODO: Convert the image to grey using cv2.cvtColor
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # TODO: Convert the image to np.float32 (divide by 255.0 first for normalization)
    frame_gray = np.float32(frame_gray / 255.0)

    # TODO: Calculate Gradients and normalize
    gx = cv2.Sobel(frame_gray, cv2.CV_32F, 1, 0, ksize=3) / 4.0
    gy = cv2.Sobel(frame_gray, cv2.CV_32F, 0, 1, ksize=3) / 4.0

    # Calculate Gradient Magnitude and normalize
    grad = np.sqrt(gx**2 + gy**2) / np.sqrt(2.0)

    # Return 3-tupel with gradient images and gradient magnitude
    return gx, gy, grad


def displayImage(gx, gy, grad):
    """
    Apply appropriate scaling and display the provided images.

    :param gx: Gradient image in X-Direction (np.float32 image with values between -1 and +1)
    :param gy: Gradient image in Y-Direction (np.float32 image with values between -1 and +1)
    :param grad: Gradient magnitude image (np.float32 image with values between 0 and 1)
    """
    # TODO: Display the gradient X and gradient Y image. Scale appropriately (values must be between 0 and 1)
    cv2.imshow("Gradient X", (0.5 * gx + 0.5))
    cv2.imshow("Gradient Y", (0.5 * gy + 0.5))

    # TODO: Display the gradient magnitude image. Scale appropriately (e.g. multiply by 4 for more contrast)
    cv2.imshow("Gradient Magnitude", 4.0 * grad)


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
        gx, gy, grad = processImage(frame)

        # TODO: Call displayImage to display the images
        displayImage(gx, gy, grad)

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
