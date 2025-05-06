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

def projection(c, skew, xh, yh):
  far = 2000.0
  near = 512.0
  return np.array([
    [c,  0.0,   0.0,  0.0],
    [0.0,  c,   0.0,  0.0],
    [0.0, 0.0,  (far + near) / (near - far), (2*far*near)/(near-far)],
    [0.0, 0.0, -1.0, 0.0]
  ]).T

def to_eucl2d_rounded(xyw):
  return (int(xyw[0] / xyw[3]), int(xyw[1] / xyw[3]))

def to_homo3d(x, y, z):
  return np.array([[x, y, z, 1.0]]).T


image_shape = (640, 640)

r = 0.0
while True:
  object_to_world = rotateX(0.05*r) @ identity_transform() # translate_3d((0.0, -256.0, 0.1))
  world_to_camera = translate_3d((0, -100, 0.01)) #@ 
  camera_to_sensor = projection(1.0 / 512.0, image_shape[0] / image_shape[1], 0.0, 0.0)
  sensor_to_image = translate_3d((image_shape[1] / 2.0, image_shape[0] / 2.0, 0.0)) @ scale((image_shape[1], image_shape[0], 1.0))

  P = sensor_to_image @ camera_to_sensor @ world_to_camera @ object_to_world
  #print(P)
  #exit()
  canvas = np.zeros(image_shape)

  for x in np.linspace(-512.0, 512.0, 20):
    for z in np.linspace(0.0, 512.0, 20):
        x1 = to_eucl2d_rounded(P @ to_homo3d(x, 0.0, z))
        cv2.circle(canvas, x1, 5, (255, 255,255))

        x1 = to_eucl2d_rounded(P @ to_homo3d(x, 512.0, z))
        cv2.circle(canvas, x1, 5, (255, 0, 0))

  cv2.imshow("Canvas", canvas)
  if cv2.waitKey(33) == 27:
    break

  r += 1
