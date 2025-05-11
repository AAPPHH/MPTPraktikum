import cv2 
import numpy as np
from enum import IntEnum

def identity_transform():
  """
  Returns the identity transformation
  """
  return np.array([
    [1.0, 0.0, 0.0, 0.0],
    [0.0, 1.0, 0.0, 0.0],
    [0.0, 0.0, 1.0, 0.0],
    [0.0, 0.0, 0.0, 1.0]])

def translate_3d(x, y, z):
  return np.array([
    [1.0, 0.0, 0.0, x],
    [0.0, 1.0, 0.0, y],
    [0.0, 0.0, 1.0, z],
    [0.0, 0.0, 0.0, 1.0],
  ])

def scale(x, y, z):
  return np.array([
    [x, 0.0, 0.0, 0.0],
    [0.0, y, 0.0, 0.0],
    [0.0, 0.0, z, 0.0],
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
    [-c, 0.0,   0.0,  0.0],
    [0.0, -c,   0.0,  0.0],
    [0.0, 0.0,  1.0,  0.0],
    [0.0, 0.0,  1.0,  0.0]
  ])

def to_homo3d(x, y, z):
  return np.array([[x, y, z, 1.0]]).T

def build_grid(xRange, zRange):
  # For now, we can only build quadratic (in number of vertices) grids
  assert len(xRange) == len(zRange)
  N = len(xRange)

  # We need N x N vertices
  vertices = np.zeros((4, N * N))
  
  # Create each vertex according to the positions in xRange and zRange
  for xIndex, xValue in enumerate(xRange):
    for zIndex, zValue in enumerate(zRange):
      index = xIndex * N + zIndex
      vertices[:, index] = to_homo3d(xValue, 0.0, zValue).flatten()

  index = 0
  # For each row, we need (N-1) segments. We have N rows in total.
  # That gives (N-1)*N segments. We need the same columnwise, so that
  # gives us (N-1)*N*2 segments in total.
  # Note that for each segment, we need two vertices!
  indices = np.zeros((N-1) * N * 2 * 2, dtype=np.int32)
  
  # Create line segments in Z direction
  for xIndex, _ in enumerate(xRange):
    for zIndex in range(N - 1):
      indices[index] = xIndex * N + zIndex
      indices[index+1] = xIndex * N + zIndex + 1
      index += 2

  # Create line segments in X direction
  for zIndex, _ in enumerate(zRange):
    for xIndex in range(N - 1):
      indices[index] = xIndex * N + zIndex
      indices[index+1] = (xIndex  + 1) * N + zIndex
      index += 2

  # A mesh is a combination of vertices and indices
  return vertices, indices

def build_cube():
  # We need 8 vertices for the cube
  vertices = np.zeros((4, 8))
  vertices[:, 0] = to_homo3d(-1.0, -1.0, -1.0).flatten()
  vertices[:, 1] = to_homo3d( 1.0, -1.0, -1.0).flatten()
  vertices[:, 2] = to_homo3d(-1.0,  1.0, -1.0).flatten()
  vertices[:, 3] = to_homo3d( 1.0,  1.0, -1.0).flatten()
  vertices[:, 4] = to_homo3d(-1.0, -1.0,  1.0).flatten()
  vertices[:, 5] = to_homo3d( 1.0, -1.0,  1.0).flatten()
  vertices[:, 6] = to_homo3d(-1.0,  1.0,  1.0).flatten()
  vertices[:, 7] = to_homo3d( 1.0,  1.0,  1.0).flatten()

  # We need 12 line segments for the cube, each segment requires 2 vertices
  indices = np.zeros(24, dtype=np.int32)
  indices[0*2 + 0], indices[0*2 + 1]   = 0, 1
  indices[1*2 + 0], indices[1*2 + 1]   = 1, 3
  indices[2*2 + 0], indices[2*2 + 1]   = 3, 2
  indices[3*2 + 0], indices[3*2 + 1]   = 2, 0

  indices[4*2 + 0], indices[4*2 + 1]   = 4, 5
  indices[5*2 + 0], indices[5*2 + 1]   = 5, 7
  indices[6*2 + 0], indices[6*2 + 1]   = 7, 6
  indices[7*2 + 0], indices[7*2 + 1]   = 6, 4

  indices[8*2 + 0], indices[8*2 + 1]   = 0, 4
  indices[9*2 + 0], indices[9*2 + 1]   = 1, 5
  indices[10*2 + 0], indices[10*2 + 1] = 2, 6
  indices[11*2 + 0], indices[11*2 + 1] = 3, 7

  return vertices, indices

def build_axis(x, y, z):
  vertices = np.zeros((4, 2))
  vertices[:, 0] = to_homo3d(0.0, 0.0, 0.0).flatten()
  vertices[:, 1] = to_homo3d(x, y, z).flatten()
  
  indices = np.zeros(2, dtype=np.int32)
  indices[0], indices[1] = 0, 1

  return vertices, indices

    
def draw(mesh, P, canvas, col):
  # Unpack mesh
  vertices, indices = mesh

  # Project all vertices into clip Space
  clipSpaceVertices = P @ vertices

  # Bring into euclidean space
  clipSpaceVertices /= clipSpaceVertices[3, :]

  # Go through list of indices
  for lineIndex in range(0, indices.shape[0], 2):
    # Indirect access
    indexA = indices[lineIndex]
    indexB = indices[lineIndex + 1]
    A = clipSpaceVertices[:, indexA]
    B = clipSpaceVertices[:, indexB]

    # If not clipped, draw line segment
    if A[2] > 0.0 and B[2] > 0.0:
      cv2.line(canvas, (int(A[0]), int(A[1])), (int(B[0]), int(B[1])), col)





gridMesh = build_grid(np.linspace(-64.0, 64.0, 9), np.linspace(-64.0, 64.0, 9))  
cubeMesh = build_cube()
axisX = build_axis(32.0, 0.0, 0.0)
axisY = build_axis(0.0, 32.0, 0.0)
axisZ = build_axis(0.0, 0.0, 32.0)

image_shape = (1024, 1024)

world_to_camera = translate_3d(0, 16.0, 164.0) @ rotateX(-0.45) @ rotateY(0.6)
camera_to_sensor = projection(1.25)
sensor_to_image = translate_3d(image_shape[1] / 2.0, image_shape[0] / 2.0, 0.0) @ scale(image_shape[1] / 2.0, image_shape[0] / 2.0, 1.0)
world_to_image = sensor_to_image @ camera_to_sensor @ world_to_camera
axis_to_world = translate_3d(-64.0, -16.0, -64.0)
grid_to_world = translate_3d(0.0, -16.0, 0.0)

class Mode(IntEnum):
  SCALE = 1
  TRANSLATE = 2
  ROTATE = 3
  ORBIT = 4

if __name__ == "__main__":
  r = 0
  mode = Mode.SCALE

  modeTexts = ["(1) Scale", "(2) Translate", "(3) Rotate", "(4) Orbit"]
  sx, sy, sz = 1.0, 1.0, 1.0
  tx, ty, tz = 0.0, 0.0, 0.0
  rx, ry, rz = 0.0, 0.0, 0.0
  ox, oy, oz = 0.0, 0.0, 0.0

  while True:
    rotate = rotateZ(rz * np.pi / 180.0) @ rotateY(ry * np.pi / 180.0) @ rotateX(rx * np.pi / 180.0)
    orbit = rotateZ(oz * np.pi / 180.0) @ rotateY(oy * np.pi / 180.0) @ rotateX(ox * np.pi / 180.0)

    local_to_world = orbit @ translate_3d(tx, ty, tz) @ rotate @ scale(sx * 16.0, sy * 16.0, sz * 16.0)
    
    

    canvas = np.zeros((image_shape[0], image_shape[1], 3))

    draw(gridMesh, world_to_image @ grid_to_world, canvas, (0.2, 0.2, 0.2))
    draw(axisX, world_to_image @ axis_to_world, canvas, (0.0, 0.0, 1.0))
    draw(axisY, world_to_image @ axis_to_world, canvas, (0.0, 1.0, 0.0))
    draw(axisZ, world_to_image @ axis_to_world, canvas, (1.0, 0.0, 0.0))
    draw(cubeMesh, world_to_image @ local_to_world, canvas, (1.0, 1.0, 1.0))
    
    for index, modeText in enumerate(modeTexts):
      x = 16 + 120 * index
      col = (1.0, 1.0, 1.0)
      if index == int(mode) - 1:
        col = (0.4, 0.6, 1.0)

        if mode == Mode.TRANSLATE:
          vx, vy, vz = tx, ty, tz

        if mode == Mode.SCALE:
          vx, vy, vz = sx, sy, sz

        if mode == Mode.ROTATE:
          vx, vy, vz = rx, ry, rz

        if mode == Mode.ORBIT:
          vx, vy, vz = ox, oy, oz

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

    dx, dy, dz = 0.0, 0.0, 0.0
    if key == ord('a'):
      dx = 1.0
    if key == ord('d'):
      dx = -1.0
    if key == ord('w'):
      dy = 1.0
    if key == ord('s'):
      dy = -1.0
    if key == ord('+'):
      dz = 1.0
    if key == ord('-'):
      dz = -1.0

    if mode == Mode.SCALE:
      sx += dx * 0.1
      sy += dy * 0.1
      sz += dz * 0.1

    if mode == Mode.TRANSLATE:
      tx += dx
      ty += dy
      tz += dz

    if mode == Mode.ROTATE:
      rx += dx
      ry += dy
      rz += dz

    if mode == Mode.ORBIT:
      ox += dx
      oy += dy
      oz += dz



    if key == 27:
      break

    r += 1
