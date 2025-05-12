import cv2 
import numpy as np
from enum import IntEnum
from misc import build_axis, build_cube, build_grid, draw

def identity_transform():
  """
  **TODO**: Return the identity transformation

  :return: Identity matrix
  :return type: 4x4 np.array
  """
  return np.array([
    [1.0, 0.0, 0.0, 0.0],
    [0.0, 1.0, 0.0, 0.0],
    [0.0, 0.0, 1.0, 0.0],
    [0.0, 0.0, 0.0, 1.0]])

def translate_3d(x, y, z):
  """
  **TODO**: Return a homogeneous translation matrix which moves coordinates by (x, y, z) as presented during lecture.

  :return: Translation matrix moving coordinates by (x, y, z)
  :return type: 4x4 np.array
  """
  return np.array([
    [1.0, 0.0, 0.0, x],
    [0.0, 1.0, 0.0, y],
    [0.0, 0.0, 1.0, z],
    [0.0, 0.0, 0.0, 1.0],
  ])

def scale(x, y, z):
  """
  **TODO**: Return a homogeneous scaling matrix which scales axes by (x, y, z) as presented during lecture.

  :return: Scaling matrix by (x, y, z)
  :return type: 4x4 np.array
  """
  return np.array([
    [x, 0.0, 0.0, 0.0],
    [0.0, y, 0.0, 0.0],
    [0.0, 0.0, z, 0.0],
    [0.0, 0.0, 0.0, 1.0],
  ])

def rotateX(radians):
  """
  **TODO**: Return a homogeneous rotation matrix which rotates around the 
  X-axis by a given amount as presented during the lecture. 

  :param radians: Angle by how far to rotate (in radians)
  :return: Rotation matrix around X-axis by given amount
  :return type: 4x4 np.array
  """
  s, c = np.sin(radians), np.cos(radians)

  return np.array([
    [1.0, 0.0, 0.0, 0.0],
    [0.0,   c,  -s, 0.0],
    [0.0,   s,   c, 0.0],
    [0.0, 0.0, 0.0, 1.0],
  ])

def rotateY(radians):
  """
  **TODO**: Return a homogeneous rotation matrix which rotates around the 
  Y-axis by a given amount as presented during the lecture. 

  :param radians: Angle by how far to rotate (in radians)
  :return: Rotation matrix around X-axis by given amount
  :return type: 4x4 np.array
  """
  s, c = np.sin(radians), np.cos(radians)

  return np.array([
    [  c, 0.0,   s, 0.0],
    [0.0, 1.0, 0.0, 0.0],
    [ -s, 0.0,   c, 0.0],
    [0.0, 0.0, 0.0, 1.0],
  ])

def rotateZ(radians):
  """
  **TODO**: Return a homogeneous rotation matrix which rotates around the 
  Z-axis by a given amount as presented during the lecture. 

  :param radians: Angle by how far to rotate (in radians)
  :return: Rotation matrix around X-axis by given amount
  :return type: 4x4 np.array
  """
  s, c = np.sin(radians), np.cos(radians)

  return np.array([
    [   c,  -s, 0.0, 0.0],
    [   s,   c, 0.0, 0.0],
    [ 0.0, 0.0, 1.0, 0.0],
    [ 0.0, 0.0, 0.0, 1.0],
  ])

def rotateXYZ(x, y, z):
  """
  **TODO** Return a combined rotation matrix which first rotates around X, then Y then Z 
  by the given amounts of radians.

  :param x: Angle to rotate around X (in radians)
  :param y: Angle to rotate around Y (in radians)
  :param z: Angle to rotate around Z (in radians)
  :return: Homogeneous matrix applying rotations around X, Y and Z 
  :return type: 4x4 np.array
  """
  return rotateZ(z) @ rotateY(y) @ rotateX(x)

def projection(c):
  """
  **TODO**: Return a projection matrix which projects along the Z-axis as presented during the lecture. 

  :param c: Focal length of pin hole camera
  :return: Projection matrix 
  :return type: 4x4 np.array
  """
  return np.array([
    [-c, 0.0,   0.0,  0.0],
    [0.0, -c,   0.0,  0.0],
    [0.0, 0.0,  1.0,  0.0],
    [0.0, 0.0,  1.0,  0.0]
  ])

def ndc_to_image(W, H):
  """
    **TODO**: Return the matrix which transforms NDC-coordinates to pixel coordinates in the final image

    Do the following transformation in this particular order
    
    For this tutorial, you can use a combination of :py:func:`translate_3d` and :py:func:`scale`
    or write the transformation matrix directly according to the script

    - Scale by (W/2, H/2, 1.0)
    - Translate by (W/2, H/2, 0.0)
  """
  return translate_3d(W / 2.0, H / 2.0, 0.0) @ scale(W / 2.0, H / 2.0, 1.0)  

def world_to_camera():
  """
  **TODO**: Return the matrix which transforms world to camera (view) coordinates. 
  For this tutorial, use a combination of :py:func:`translate_3d`,
  :py:func:`rotateX` and :py:func:`rotateY`.

  Do the following transformation in this particular order

  - Rotate around Y by 35 degrees.
  - Rotate around X by -30 degrees
  - Translate by (0, 16, 164)

  **Hint**: You can use `np.deg2rad <https://numpy.org/doc/2.1/reference/generated/numpy.deg2rad.html>`_ to convert degrees to radians. 

  :return: Homogeneous matrix defining the transformation from world to camera coordinate space
  :return type: 4x4 np.array
  """
  return translate_3d(0, 16.0, 164.0) @ rotateX(np.deg2rad(-30.0)) @ rotateY(np.deg2rad(35.0))

def world_to_image(W, H, c):
  """
  **TODO**: Return the complete projection matrix mapping from world coordinates to image coordinates.
  This is a concatenation of the `world_to_camera` matrix, the projection matrix and the mapping from 
  NDC to image coordinates. Do the following transformations in the particular order

  - Map :py:func:`world_to_camera` by calling the respective function
  - Project along the z axis by calling :py:func:`projection`
  - Map :py:func:`ndc_to_image` by calling the respective function

  :return: Homogeneous matrix defining the transformation from world to image coordinates
  :return type: 4x4 np.array
  """
  return ndc_to_image(W, H) @ projection(c) @ world_to_camera()

def local_to_world(objectScale, objectRotate, objectTranslate, objectOrbit):
  return rotateXYZ(objectOrbit[0], objectOrbit[1], objectOrbit[2]) @\
         translate_3d(objectTranslate[0], objectTranslate[1], objectTranslate[2]) @\
         rotateXYZ(objectRotate[0], objectRotate[1], objectRotate[2]) @\
         scale(objectScale[0], objectScale[1], objectScale[2])




gridMesh = build_grid(np.linspace(-64.0, 64.0, 9), np.linspace(-64.0, 64.0, 9))  
cubeMesh = build_cube()
axisX = build_axis(32.0, 0.0, 0.0)
axisY = build_axis(0.0, 32.0, 0.0)
axisZ = build_axis(0.0, 0.0, 32.0)

image_shape = (1024, 1024)

w2i = world_to_image(image_shape[1], image_shape[0], 1.25)

axis_to_world = translate_3d(-64.0, -16.0, -64.0)
grid_to_world = translate_3d(0.0, -16.0, 0.0)

class Mode(IntEnum):
  SCALE = 1
  TRANSLATE = 2
  ROTATE = 3
  ORBIT = 4

if __name__ == "__main__":
  mode = Mode.SCALE

  modeTexts = ["(1) Scale", "(2) Translate", "(3) Rotate", "(4) Orbit"]

  objectScale = np.array([16.0, 16.0, 16.0])
  objectTranslate = np.array([0.0, 0.0, 0.0])
  objectRotate = np.array([0.0, 0.0, 0.0])
  objectOrbit = np.array([0.0, 0.0, 0.0])

  while True:
    cube_to_world = local_to_world(objectScale, objectRotate, objectTranslate, objectOrbit)
    
    canvas = np.zeros((image_shape[0], image_shape[1], 3))

    draw(gridMesh, w2i @ grid_to_world, canvas, (0.2, 0.2, 0.2))
    draw(axisX, w2i @ axis_to_world, canvas, (0.0, 0.0, 1.0))
    draw(axisY, w2i @ axis_to_world, canvas, (0.0, 1.0, 0.0))
    draw(axisZ, w2i @ axis_to_world, canvas, (1.0, 0.0, 0.0))
    draw(cubeMesh, w2i @ cube_to_world, canvas, (1.0, 1.0, 1.0))
    
    for index, modeText in enumerate(modeTexts):
      x = 16 + 120 * index
      col = (1.0, 1.0, 1.0)
      if index == int(mode) - 1:
        col = (0.4, 0.6, 1.0)

        if mode == Mode.TRANSLATE:
          vx, vy, vz = objectTranslate[0], objectTranslate[1], objectTranslate[2]

        if mode == Mode.SCALE:
          vx, vy, vz = objectScale[0], objectScale[1], objectScale[2]

        if mode == Mode.ROTATE:
          vx, vy, vz = np.rad2deg(objectRotate[0]), np.rad2deg(objectRotate[1]), np.rad2deg(objectRotate[2])

        if mode == Mode.ORBIT:
          vx, vy, vz = np.rad2deg(objectOrbit[0]), np.rad2deg(objectOrbit[1]), np.rad2deg(objectOrbit[2])

        cv2.putText(canvas, f"{vx:.2f}, {vy:.2f}, {vz:.2f}", (x, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0.7, 0.7, 0.7), 2)
      
      cv2.putText(canvas, modeText, (x, 16), cv2.FONT_HERSHEY_SIMPLEX, 0.5, col, 2)

    cv2.imshow("Canvas", canvas)

    key = cv2.waitKey(33)
    if key == ord('1'):
      mode = Mode.SCALE

    if key == ord('2'):
      mode = Mode.TRANSLATE

    if key == ord('3'):
      mode = Mode.ROTATE

    if key == ord('4'):
      mode = Mode.ORBIT

    delta = np.array([0.0, 0.0, 0.0])
    if key == ord('a'):
      delta[0] = 1.0
    if key == ord('d'):
      delta[0] = -1.0
    if key == ord('w'):
      delta[1] = 1.0
    if key == ord('s'):
      delta[1] = -1.0
    if key == ord('+'):
      delta[2] = 1.0
    if key == ord('-'):
      delta[2] = -1.0

    if mode == Mode.SCALE:
      objectScale += delta

    if mode == Mode.TRANSLATE:
      objectTranslate += delta

    if mode == Mode.ROTATE:
      objectRotate += np.deg2rad(delta)

    if mode == Mode.ORBIT:
      objectOrbit += delta

    if key == 27:
      break
