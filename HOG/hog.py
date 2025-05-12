import os
import cv2
import numpy as np


def calculate_gradient_directions(totalDirections=12, offset=0.0):
    angles = np.linspace(0, 2.0 * np.pi, totalDirections, endpoint=False) + offset
    hogDirections = np.zeros((2, totalDirections))

    hogDirections[0, :] = np.cos(angles)
    hogDirections[1, :] = np.sin(angles)

    return hogDirections


def hog_cell(magnitude, winningBin, totalDirections):
    cellVector = np.zeros(totalDirections)
    for index in range(totalDirections):
        cellVector[index] = magnitude[winningBin == index].sum()

    return cellVector / 256.0  # / np.linalg.norm(cellVector)


def visualize_hog_cell(cellVector, directions, shape=(16, 16)):
    cell = np.zeros(shape)
    W, H = shape[0], shape[1]
    for index, value in enumerate(cellVector):
        dx, dy = directions[0, index], directions[1, index]

        x0, y0 = int(W // 2), int(H // 2)
        x1, y1 = int(x0 + dx * W / 2), int(y0 + dy * H / 2)
        cv2.line(cell, (x0, y0), (x1, y1), (value, value, value))

    return cell


def process_hog(gray, totalDirections=12):
    hogDirections = calculate_gradient_directions(totalDirections)

    gx = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=5)
    gy = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=5)
    mag = np.sqrt(gx**2 + gy**2)

    gx, gy = gx.flatten(), gy.flatten()
    winningBin, bestDot = np.zeros_like(gx), np.zeros_like(gx)
    for direction in range(totalDirections):
        dot = gx * hogDirections[0, direction] + gy * hogDirections[1, direction]

        greaterIndices = dot > bestDot
        winningBin[greaterIndices] = direction
        bestDot[greaterIndices] = dot[greaterIndices]

    winningBin = winningBin.reshape(gray.shape)

    binGray = np.uint8(255 * winningBin / (totalDirections - 1))
    binColor = cv2.applyColorMap(binGray, cv2.COLORMAP_JET)
    binColor[mag < 1.5] = (0, 0, 0)

    cv2.imshow("Gradient Direction", binColor)

    # cellSize = 8
    # hogImage = np.zeros_like(gray)
    # for x0 in range(0, gray.shape[1], cellSize):
    #    for y0 in range(0, gray.shape[0], cellSize):
    #       x1, y1 = x0 + cellSize, y0 + cellSize

    #       cellVector = hog_cell(mag[y0:y1, x0:x1], winningBin[y0:y1, x0:x1], totalDirections)
    #       img = visualize_hog_cell(cellVector, hogDirections, (cellSize, cellSize))

    #       hogImage[y0:y1, x0:x1] = img

    # cv2.imshow("HOG Vector", hogImage)


if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # if frame is read correctly ret is True
        if not ret:
            exit()

        # Convert image to gray scale
        gray = np.float32(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) / 255.0)

        process_hog(gray)

        # Display the resulting frame
        if cv2.waitKey(1) == ord("q"):
            break
