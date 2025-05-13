import numpy as np
import cv2



def displayImage(image):
  scaled = cv2.resize(image, (512, 512), interpolation=cv2.INTER_NEAREST)
  cv2.imshow("Original Image", scaled)

def drawEdge(image, normalVector):
  for xIndex, xValue in enumerate(np.linspace(-0.5, 0.5, image.shape[1])):
    for yIndex, yValue in enumerate(np.linspace(-0.5, 0.5, image.shape[0])):
      dot = xValue * normalVector[0] + yValue * normalVector[1]
      if dot > 0.0:
        image[yIndex, xIndex] = 1.0

  return image

def main():
  mainAxis = np.array([1.0, 0.0])
  secondaryAxis = np.array([1.0, 0.0])
  while True:
    image = np.random.normal(0.5, 0.1, (64,64))
    drawEdge(image, mainAxis)
    drawEdge(image, secondaryAxis)
    image += np.random.normal(0.0, 0.1, (64,64))

    displayImage(image)

    key = cv2.waitKey(0)
    if key == 27:
      break

    if key == ord("+"):
      c = np.cos(np.deg2rad(5.0))
      s = np.sin(np.deg2rad(5.0))
      mainAxis = (np.array([[c, -s],[s, c]]) @ np.array([[mainAxis[0], mainAxis[1]]]).T).flatten()

    if key == ord("-"):
      c = np.cos(np.deg2rad(-5.0))
      s = np.sin(np.deg2rad(-5.0))
      mainAxis = (np.array([[c, -s],[s, c]]) @ np.array([[mainAxis[0], mainAxis[1]]]).T).flatten()

    if key == ord("*"):
      c = np.cos(np.deg2rad(5.0))
      s = np.sin(np.deg2rad(5.0))
      secondaryAxis = (np.array([[c, -s],[s, c]]) @ np.array([[secondaryAxis[0], secondaryAxis[1]]]).T).flatten()

    if key == ord("/"):
      c = np.cos(np.deg2rad(-5.0))
      s = np.sin(np.deg2rad(-5.0))
      secondaryAxis = (np.array([[c, -s],[s, c]]) @ np.array([[secondaryAxis[0], secondaryAxis[1]]]).T).flatten()




if __name__ == "__main__":
  main()