import numpy as np
import cv2

def to_homo3d(x, y, z):
  """
  Returns homogeneous 3D coordinates
  """
  return np.array([x, y, z, 1.0]).T

def build_grid(xRange, zRange):
  """
  Builds a regular grid mesh
  """
  # For now, we can only build quadratic (in number of vertices) grids
  assert len(xRange) == len(zRange)
  N = len(xRange)

  # We need N x N vertices
  vertices = np.zeros((4, N * N))
  
  # Create each vertex according to the positions in xRange and zRange
  for xIndex, xValue in enumerate(xRange):
    for zIndex, zValue in enumerate(zRange):
      index = xIndex * N + zIndex
      vertices[:, index] = to_homo3d(xValue, 0.0, zValue)

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
  """
  Builds a 6 sides cube mesh
  """
  # We need 8 vertices for the cube
  vertices = np.zeros((4, 8))
  vertices[:, 0] = to_homo3d(-1.0, -1.0, -1.0)
  vertices[:, 1] = to_homo3d( 1.0, -1.0, -1.0)
  vertices[:, 2] = to_homo3d(-1.0,  1.0, -1.0)
  vertices[:, 3] = to_homo3d( 1.0,  1.0, -1.0)
  vertices[:, 4] = to_homo3d(-1.0, -1.0,  1.0)
  vertices[:, 5] = to_homo3d( 1.0, -1.0,  1.0)
  vertices[:, 6] = to_homo3d(-1.0,  1.0,  1.0)
  vertices[:, 7] = to_homo3d( 1.0,  1.0,  1.0)

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
  """
  Builds a simple axis mesh
  """
  vertices = np.zeros((4, 2))
  vertices[:, 0] = to_homo3d(0.0, 0.0, 0.0)
  vertices[:, 1] = to_homo3d(x, y, z)
  
  indices = np.zeros(2, dtype=np.int32)
  indices[0], indices[1] = 0, 1

  return vertices, indices


def draw(mesh, P, canvas, col):
  """
  Draws a given mesh using the provided projection matrix into the given canvas using provided color
  """
  # Unpack mesh
  vertices, indices = mesh

  # Project all vertices into image coordinates
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

