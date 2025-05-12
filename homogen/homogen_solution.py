import cv2
import numpy as np
from misc import build_axis, build_cube, build_grid, Mode


def translate_3d(x, y, z):
    """
    **TODO**: Return a homogeneous translation matrix which moves coordinates by (x, y, z) as presented during lecture.

    :return: Translation matrix moving coordinates by (x, y, z)
    :return type: 4x4 np.array
    """
    return np.array(
        [
            [1.0, 0.0, 0.0, x],
            [0.0, 1.0, 0.0, y],
            [0.0, 0.0, 1.0, z],
            [0.0, 0.0, 0.0, 1.0],
        ]
    )


def scale(x, y, z):
    """
    **TODO**: Return a homogeneous scaling matrix which scales axes by (x, y, z) as presented during lecture.

    :return: Scaling matrix by (x, y, z)
    :return type: 4x4 np.array
    """
    return np.array(
        [
            [x, 0.0, 0.0, 0.0],
            [0.0, y, 0.0, 0.0],
            [0.0, 0.0, z, 0.0],
            [0.0, 0.0, 0.0, 1.0],
        ]
    )


def rotateX(radians):
    """
    **TODO**: Return a homogeneous rotation matrix which rotates around the
    X-axis by a given amount as presented during the lecture.

    :param radians: Angle by how far to rotate (in radians)
    :return: Rotation matrix around X-axis by given amount
    :return type: 4x4 np.array
    """
    s, c = np.sin(radians), np.cos(radians)

    return np.array(
        [
            [1.0, 0.0, 0.0, 0.0],
            [0.0, c, -s, 0.0],
            [0.0, s, c, 0.0],
            [0.0, 0.0, 0.0, 1.0],
        ]
    )


def rotateY(radians):
    """
    **TODO**: Return a homogeneous rotation matrix which rotates around the
    Y-axis by a given amount as presented during the lecture.

    :param radians: Angle by how far to rotate (in radians)
    :return: Rotation matrix around X-axis by given amount
    :return type: 4x4 np.array
    """
    s, c = np.sin(radians), np.cos(radians)

    return np.array(
        [
            [c, 0.0, s, 0.0],
            [0.0, 1.0, 0.0, 0.0],
            [-s, 0.0, c, 0.0],
            [0.0, 0.0, 0.0, 1.0],
        ]
    )


def rotateZ(radians):
    """
    **TODO**: Return a homogeneous rotation matrix which rotates around the
    Z-axis by a given amount as presented during the lecture.

    :param radians: Angle by how far to rotate (in radians)
    :return: Rotation matrix around X-axis by given amount
    :return type: 4x4 np.array
    """
    s, c = np.sin(radians), np.cos(radians)

    return np.array(
        [
            [c, -s, 0.0, 0.0],
            [s, c, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0],
        ]
    )


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
    return np.array(
        [
            [-c, 0.0, 0.0, 0.0],
            [0.0, -c, 0.0, 0.0],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0, 0.0],
        ]
    )


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
    return (
        translate_3d(0, 16.0, 164.0)
        @ rotateX(np.deg2rad(-30.0))
        @ rotateY(np.deg2rad(35.0))
    )


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
    """
    **TODO**: Return the transformation from local coordinates to world coordinates.
    Apply the following transformations in this particular order

    - Scale by the parameters provided in objectScale
    - Rotate by the parameters provided in objectRotate
    - Translate by the parameters provided in objectTranslate
    - Rotate again by the parameters provided in objectOrbit.

    *Note*: Because the second rotation happens after the translation it will "orbit" around the
    center.

    :param objectScale: 3 element array with scaling parameters
    :param objectRotate: 3 element array with rotation parameters (in radians)
    :param objectTranslate: 3 element array with translation parameters
    :param objectOrbit: 3 element array with orbiting parameters (in radians)
    """
    return (
        rotateXYZ(objectOrbit[0], objectOrbit[1], objectOrbit[2])
        @ translate_3d(objectTranslate[0], objectTranslate[1], objectTranslate[2])
        @ rotateXYZ(objectRotate[0], objectRotate[1], objectRotate[2])
        @ scale(objectScale[0], objectScale[1], objectScale[2])
    )


def project_vertexbuffer(local_to_image, vertices):
    """
    **TODO**: Project all vertices in the provided vertex buffer using the given transformation
    and convert to euclidean coordinates by dividing by the w-component of each vertex.

    :param vertices: Vertex buffer (4xN Matrix)
    :param local_to_image: Transformation matrix to apply (4x4 Matrix)
    :return: Transformed vertices in euclidean space (w == 1)
    """
    # First, project all vertices using the given transformation
    vertices = local_to_image @ vertices

    # Now divide by w to convert to euclidean coordinates
    vertices /= vertices[3, :]

    return vertices


def draw(mesh, local_to_image, canvas, col):
    """
    Draws a given mesh using the provided projection matrix into the given canvas using provided color.

    :param mesh: 2-Tuple (vertices, indices) containing both the vertex buffer as well as the index buffer
    :param local_to_image: Transformation matrix to transform vertices from local space to image space
    :param canvas: OpenCV image to draw into (3 channel RGB, np.float32)
    :param col: Color to draw (3-Tuple with (B, G, R) color intensities ranging from 0.0 to 1.0 each)
    """
    # Unpack mesh
    vertices, indices = mesh

    # Project vertices
    vertices = project_vertexbuffer(local_to_image, vertices)

    # Go through list of indices
    for lineIndex in range(0, indices.shape[0], 2):
        # Indirect access
        indexA = indices[lineIndex]
        indexB = indices[lineIndex + 1]
        A = vertices[:, indexA]
        B = vertices[:, indexB]

        cv2.line(canvas, (int(A[0]), int(A[1])), (int(B[0]), int(B[1])), col)


# Geschafft, ab hier brauchen Sie nichts mehr zu implementieren!
if __name__ == "__main__":
    # Wir starten im Modus "Verschiebung"
    mode = Mode.TRANSLATE

    # Erzeuge die Meshes für das Koordinatensystem, den Würfel und die Achsen
    gridMesh = build_grid(np.linspace(-64.0, 64.0, 9), np.linspace(-64.0, 64.0, 9))
    cubeMesh = build_cube()
    axisX = build_axis(32.0, 0.0, 0.0)
    axisY = build_axis(0.0, 32.0, 0.0)
    axisZ = build_axis(0.0, 0.0, 32.0)

    # Unser Bild soll 1024x1024 Pixel haben
    image_shape = (1024, 1024)

    # Wir brauchen die zentrale Transformation von Weltkoordinaten nach Bildkoordinaten
    w2i = world_to_image(image_shape[1], image_shape[0], 1.25)

    # Die Welt-Transformation der Achsen (passend verschoben)
    axis_to_world = translate_3d(-64.0, -16.0, -64.0)

    # Die Welt-Transformation des Koordinatensystems (nach unten verschoben)
    grid_to_world = translate_3d(0.0, -16.0, 0.0)

    # Die Texte im UI
    modeTexts = ["(1) Scale", "(2) Translate", "(3) Rotate", "(4) Orbit"]

    # Anfangsparameter für die Objekttransformation des Würfels
    objectScale = np.array([16.0, 16.0, 16.0])
    objectTranslate = np.array([0.0, 0.0, 0.0])
    objectRotate = np.array([0.0, 0.0, 0.0])
    objectOrbit = np.array([0.0, 0.0, 0.0])

    # Endloßßschleife (mit ESC unterbrechen)
    while True:
        # Baue die aktuelle Welt-Transformation für den Würfel
        cube_to_world = local_to_world(
            objectScale, objectRotate, objectTranslate, objectOrbit
        )

        # Starte mit einem leeren (schwarzen) Bild
        canvas = np.zeros((image_shape[0], image_shape[1], 3))

        # Zeichne die verschiedenen Komponenten in ihren jeweiligen Farben.
        # Verwende dabei die passenden Transformationen
        draw(gridMesh, w2i @ grid_to_world, canvas, (0.2, 0.2, 0.2))
        draw(axisX, w2i @ axis_to_world, canvas, (0.0, 0.0, 1.0))
        draw(axisY, w2i @ axis_to_world, canvas, (0.0, 1.0, 0.0))
        draw(axisZ, w2i @ axis_to_world, canvas, (1.0, 0.0, 0.0))
        draw(cubeMesh, w2i @ cube_to_world, canvas, (1.0, 1.0, 1.0))

        # Zeichne das User-Interface
        for index, modeText in enumerate(modeTexts):
            x = 16 + 120 * index
            col = (1.0, 1.0, 1.0)
            if index == int(mode) - 1:
                col = (0.4, 0.6, 1.0)

                if mode == Mode.TRANSLATE:
                    vx, vy, vz = (
                        objectTranslate[0],
                        objectTranslate[1],
                        objectTranslate[2],
                    )

                if mode == Mode.SCALE:
                    vx, vy, vz = objectScale[0], objectScale[1], objectScale[2]

                if mode == Mode.ROTATE:
                    vx, vy, vz = (
                        np.rad2deg(objectRotate[0]),
                        np.rad2deg(objectRotate[1]),
                        np.rad2deg(objectRotate[2]),
                    )

                if mode == Mode.ORBIT:
                    vx, vy, vz = (
                        np.rad2deg(objectOrbit[0]),
                        np.rad2deg(objectOrbit[1]),
                        np.rad2deg(objectOrbit[2]),
                    )

                cv2.putText(
                    canvas,
                    f"{vx:.2f}, {vy:.2f}, {vz:.2f}",
                    (x, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0.7, 0.7, 0.7),
                    2,
                )

            cv2.putText(
                canvas, modeText, (x, 16), cv2.FONT_HERSHEY_SIMPLEX, 0.5, col, 2
            )

        # Übergebe das Bild ans Betriebssystem und warte auf einen Tastendruck
        cv2.imshow("Canvas", canvas)

        key = cv2.waitKey(0)
        if key == ord("1"):
            mode = Mode.SCALE

        if key == ord("2"):
            mode = Mode.TRANSLATE

        if key == ord("3"):
            mode = Mode.ROTATE

        if key == ord("4"):
            mode = Mode.ORBIT

        delta = np.array([0.0, 0.0, 0.0])
        if key == ord("a"):
            delta[0] = 1.0
        if key == ord("d"):
            delta[0] = -1.0
        if key == ord("w"):
            delta[1] = 1.0
        if key == ord("s"):
            delta[1] = -1.0
        if key == ord("+"):
            delta[2] = 1.0
        if key == ord("-"):
            delta[2] = -1.0

        if mode == Mode.SCALE:
            objectScale += delta

        if mode == Mode.TRANSLATE:
            objectTranslate += delta

        if mode == Mode.ROTATE:
            objectRotate += np.deg2rad(delta)

        if mode == Mode.ORBIT:
            objectOrbit += np.deg2rad(delta)

        if key == 27:
            break
