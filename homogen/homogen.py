import cv2 
import numpy as np

def identity_transform():
  return np.array([
    [1.0, 0.0, 0.0, 0.0],
    [0.0, 1.0, 0.0, 0.0],
    [0.0, 0.0, 1.0, 0.0],
    [0.0, 0.0, 0.0, 1.0]])

def translate_3d(xyz):
  return np.array([
    [1.0, 0.0, 0.0, xyz[0]],
    [0.0, 1.0, 0.0, xyz[1]],
    [0.0, 0.0, 1.0, xyz[2]],
    [0.0, 0.0, 0.0, 1.0],
  ])

def translate_2d(xyz):
  return np.array([
    [1.0, 0.0, xyz[0], 0.0],
    [0.0, 1.0, xyz[1], 0.0],
    [0.0, 0.0, 1.0, 0.0],
    [0.0, 0.0, 0.0, 1.0],
  ])

def scale(xyz):
  return np.array([
    [xyz[0], 0.0, 0.0, 0.0],
    [0.0, xyz[1], 0.0, 0.0],
    [0.0, 0.0, xyz[2], 0.0],
    [0.0, 0.0, 0.0, 1.0],
  ])

def rotateX(radians):
  s, c = np.sin(radians), np.cos(radians)

  return np.array([
    [1.0, 0.0, 0.0, 0.0],
    [0.0,   c,  -s, 0.0],
    [0.0,   s,   c, 0.0],
    [0.0, 0.0, 0.0, 1.0],
  ])

def rotateY(radians):
  s, c = np.sin(radians), np.cos(radians)

  return np.array([
    [  c, 0.0,   s, 0.0],
    [0.0, 1.0, 0.0, 0.0],
    [ -s, 0.0,   c, 0.0],
    [0.0, 0.0, 0.0, 1.0],
  ])

def rotateZ(radians):
  s, c = np.sin(radians), np.cos(radians)

  return np.array([
    [   c,  -s, 0.0, 0.0],
    [   s,   c, 0.0, 0.0],
    [ 0.0, 0.0, 1.0, 0.0],
    [ 0.0, 0.0, 0.0, 1.0],
  ])

def projection(c):
  return np.array([
    [c,  0.0,   0.0,  0.0],
    [0.0,  c,   0.0,  0.0],
    [0.0, 0.0,  -1, -2.0],
    [0.0, 0.0, -1.0, 0.0]
  ]).T

def to_eucl2d_rounded(xyw):
  return (int(xyw[0] / xyw[3]), int(xyw[1] / xyw[3])), (xyw[2] / xyw[3]).item()

def to_homo3d(x, y, z):
  return np.array([[x, y, z, 1.0]]).T


image_shape = (640, 640)

r = 0
while True:
  object_to_world = identity_transform() @ rotateY(0.002 * r) @ rotateX(0.02 * r) @ identity_transform()
  world_to_camera = translate_3d((0, -16.0, 164.0)) @ rotateX(-0.5)
  camera_to_sensor = projection(1.73, image_shape[0] / image_shape[1], 0.0, 0.0)
  sensor_to_image = translate_3d((image_shape[1] / 2.0, image_shape[0] / 2.0, 0.0)) @ scale((image_shape[1], image_shape[0], 1.0))

  P = sensor_to_image @ camera_to_sensor @ world_to_camera @ object_to_world
  canvas = np.zeros(image_shape)

  for x in np.linspace(-64.0, 64.0, 16):
    for z in np.linspace(-64.0, 64.0, 16):  
      x1, zClip1= to_eucl2d_rounded(P @ to_homo3d(x, 0.0, z))
      x2, zClip2 = to_eucl2d_rounded(P @ to_homo3d(x + 8.0, 0.0, z))
      x3, zClip3 = to_eucl2d_rounded(P @ to_homo3d(x, 0.0, z + 8.0))
      if zClip1 > 0.5 and zClip2 > 0.5 and zClip3 > 0.5:
        cv2.line(canvas, x1, x2, 255)
        cv2.line(canvas, x1, x3, 255)
        #cv2.circle(canvas, x1, 5, (255, 255,255))

  cv2.imshow("Canvas", canvas)
  if cv2.waitKey(33) == 27:
    break

  r += 1
