import numpy as np
import cv2


def displayImage(image):
    scaled = cv2.resize(image, (512, 512), interpolation=cv2.INTER_NEAREST)
    cv2.imshow("Original Image", scaled)


def drawEdge(image, mainAxis, secondaryAxis, col):
    T = 0.05
    for xIndex, xValue in enumerate(np.linspace(-0.5, 0.5, image.shape[1])):
        for yIndex, yValue in enumerate(np.linspace(-0.5, 0.5, image.shape[0])):
            dot1 = xValue * mainAxis[0] + yValue * mainAxis[1]
            dot2 = xValue * secondaryAxis[0] + yValue * secondaryAxis[1]
            dot = min(dot1, dot2)
            if dot > T:
                image[yIndex, xIndex] = col
            elif dot > -T:
                alpha = (dot + T) / (2 * T)
                c = alpha * col + (1 - alpha) * (1 - col)
                image[yIndex, xIndex] = c

    return image


def gradientScatterPlot(image, plot):
    # Calculate Gradient and clip
    gx = np.clip(cv2.Sobel(image, cv2.CV_32F, 1, 0, ksize=3) / 2.0, -1.0, 1.0).flatten()
    gy = np.clip(cv2.Sobel(image, cv2.CV_32F, 0, 1, ksize=3) / 2.0, -1.0, 1.0).flatten()

    vx = np.sum(gx**2)
    vy = np.sum(gy**2)
    cov = np.sum(gx * gy)

    M = np.array([[vx, cov], [cov, vy]])
    L = np.linalg.cholesky(M)

    R = (vx * vy - cov**2) - 0.04 * (vx + vy) ** 2

    # Project into plot image, cast to integer and flatten
    gx = np.int32((gx + 1.0) / 2.0 * (plot.shape[1] - 1))
    gy = np.int32((gy + 1.0) / 2.0 * (plot.shape[0] - 1))

    # Now draw
    for x, y in zip(gx, gy):
        cv2.circle(plot, (x, y), 2, (0.0, 0.0, 1.0), -1)

    # Draw ellipse
    x2, y2 = None, None
    for angle in np.linspace(0.0, 2.0 * np.pi, 360):
        s, c = np.sin(angle), np.cos(angle)
        v = L @ np.array([[s, c]]).T
        v *= 0.01 * plot.shape[0]
        x1, y1 = int(v[0] + plot.shape[1] / 2), int(v[1] + plot.shape[0] / 2)
        if x2 is not None:
            cv2.line(plot, (x1, y1), (x2, y2), (1.0, 0.0, 0.0), 2)
        x2, y2 = x1, y1

    # Draw Corner Strength
    cv2.putText(
        plot,
        f"R = {R:.2f}",
        (16, 16),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (0.9, 0.8, 0.7),
        2,
    )


def main():
    shape = (64, 64)
    mainAxis = np.array([1.0, 0.0])
    secondaryAxis = np.array([1.0, 0.0])
    alpha = 0.95
    noise_pattern = np.random.normal(0.0, 1.0 - alpha, shape)
    while True:
        # Construct the image edges or corners and noise
        image = np.zeros(shape, dtype=np.float32)
        drawEdge(image, mainAxis, secondaryAxis, 1.0)
        image += 0.3 * noise_pattern
        image = cv2.blur(image, ksize=(3, 3))
        noise_pattern = (alpha**2) * noise_pattern + np.random.normal(
            0.0, 1 - alpha, shape
        )

        # Calculate Gradient Scatter plot
        plot = np.zeros((512, 512, 3))
        gradientScatterPlot(image, plot)

        cv2.imshow("Gradient Scatter Plot", plot)
        # Display it
        displayImage(image)

        key = cv2.waitKey(0)
        if key == 27:
            break

        if key == ord("+") or key == ord("w"):
            c = np.cos(np.deg2rad(5.0))
            s = np.sin(np.deg2rad(5.0))
            mainAxis = (
                np.array([[c, -s], [s, c]]) @ np.array([[mainAxis[0], mainAxis[1]]]).T
            ).flatten()

        if key == ord("-") or key == ord("s"):
            c = np.cos(np.deg2rad(-5.0))
            s = np.sin(np.deg2rad(-5.0))
            mainAxis = (
                np.array([[c, -s], [s, c]]) @ np.array([[mainAxis[0], mainAxis[1]]]).T
            ).flatten()

        if key == ord("*") or key == ord("w"):
            c = np.cos(np.deg2rad(5.0))
            s = np.sin(np.deg2rad(5.0))
            secondaryAxis = (
                np.array([[c, -s], [s, c]])
                @ np.array([[secondaryAxis[0], secondaryAxis[1]]]).T
            ).flatten()

        if key == ord("/") or key == ord("s"):
            c = np.cos(np.deg2rad(-5.0))
            s = np.sin(np.deg2rad(-5.0))
            secondaryAxis = (
                np.array([[c, -s], [s, c]])
                @ np.array([[secondaryAxis[0], secondaryAxis[1]]]).T
            ).flatten()


if __name__ == "__main__":
    main()
