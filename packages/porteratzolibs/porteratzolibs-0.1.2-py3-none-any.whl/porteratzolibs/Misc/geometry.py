import numpy as np


def point_dis(a, b=None):
    if b is not None:
        c = a - b
    else:
        c = a
    anorm = np.sqrt(np.sum(np.multiply(c, c)))
    return anorm

def angle_b_vectors(a, b):
    value = np.sum(np.multiply(a, b)) / (np.linalg.norm(a) * np.linalg.norm(b))
    if (value < -1) | (value > 1):
        value = np.sign(value)
    angle = np.arccos(value)
    return angle


def getPrincipalVectors(
    A,
):  # get pricipal vectors and values of a matrix centered around (0,0,0)
    VT = np.linalg.eig(np.matmul(A.T, A))
    sort = sorted(zip(VT[0], VT[1].T.tolist()), reverse=True)
    Values, Vectors = zip(*sort)
    return Vectors, Values


def Dpoint2Plane(
    point, planecoefs
):  # get minimum distance from a point to a plane
    return (
        planecoefs[0] * point[0]
        + planecoefs[1] * point[1]
        + planecoefs[2] * point[2]
        + planecoefs[3]
    ) / np.linalg.norm(planecoefs[0:3])


def DistPoint2Line(
    point, linepoint1, linepoint2=np.array([0, 0, 0])
):  # get minimum destance from a point to a line
    return np.linalg.norm(
        np.cross((point - linepoint2), (point - linepoint1))
    ) / np.linalg.norm(linepoint1 - linepoint2)


def rotation_matrix_from_vectors(vec1, vec2):
    if all(np.abs(vec1) == np.abs(vec2)):
        return np.eye(3)
    a, b = (vec1 / np.linalg.norm(vec1)).reshape(3), (
        vec2 / np.linalg.norm(vec2)
    ).reshape(3)
    v = np.cross(a, b)
    c = np.dot(a, b)
    s = np.linalg.norm(v)
    kmat = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    rotation_matrix = np.eye(3) + kmat + kmat.dot(kmat) * ((1 - c) / (s ** 2))
    return rotation_matrix





