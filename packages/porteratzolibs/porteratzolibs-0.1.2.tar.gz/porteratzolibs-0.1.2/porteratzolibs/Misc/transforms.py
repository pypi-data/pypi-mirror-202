import numpy as np
import math


def SVDRigidBodyTransform(Points1, points2):
    centroid1 = np.sum(Points1, 0) / len(Points1)
    centroid2 = np.sum(points2, 0) / len(points2)
    CenteredVector1 = (Points1 - centroid1).transpose()
    CenteredVector2 = (points2 - centroid2).transpose()

    YiT = CenteredVector2.transpose()
    Xi = CenteredVector1
    Wi = np.eye(Xi.shape[1])

    S = np.matmul(Xi, np.matmul(Wi, YiT))
    U, SigNDiag, VT = np.linalg.svd(S, full_matrices=True)
    Raro = np.eye(3)
    Raro[-1, -1] = np.linalg.det(np.matmul(VT.transpose(), U.transpose()))

    RotacionFinal = np.matmul(VT.transpose(), np.matmul(Raro, U.transpose()))
    traslation = (centroid2 - np.matmul(RotacionFinal, centroid1)).reshape(
        3, 1
    )
    return traslation, RotacionFinal

def SVDLstSqr(X, Y):
    U, s, VT = np.linalg.svd(X)
    S = np.diag(s)
    Si = np.zeros([U.shape[1], VT.shape[0]])
    Si[0 : S.shape[0], 0 : S.shape[0]] = np.diag(1 / s)
    return np.matmul(VT.T, np.matmul(Si.T, np.matmul(U.T, Y)))

def eulerAnglesToRotationMatrix(theta):
    R_x = np.array(
        [
            [1, 0, 0],
            [0, np.cos(theta[0]), -np.sin(theta[0])],
            [0, np.sin(theta[0]), np.cos(theta[0])],
        ]
    )
    R_y = np.array(
        [
            [np.cos(theta[1]), 0, np.sin(theta[1])],
            [0, 1, 0],
            [-np.sin(theta[1]), 0, np.cos(theta[1])],
        ]
    )
    R_z = np.array(
        [
            [np.cos(theta[2]), -np.sin(theta[2]), 0],
            [np.sin(theta[2]), np.cos(theta[2]), 0],
            [0, 0, 1],
        ]
    )
    R = np.dot(R_z, np.dot(R_y, R_x))
    return R


def eulerAnglesToRotationMatrixZYX(theta):
    R_x = np.array(
        [
            [1, 0, 0],
            [0, np.cos(theta[0]), -np.sin(theta[0])],
            [0, np.sin(theta[0]), np.cos(theta[0])],
        ]
    )
    R_y = np.array(
        [
            [np.cos(theta[1]), 0, np.sin(theta[1])],
            [0, 1, 0],
            [-np.sin(theta[1]), 0, np.cos(theta[1])],
        ]
    )
    R_z = np.array(
        [
            [np.cos(theta[2]), -np.sin(theta[2]), 0],
            [np.sin(theta[2]), np.cos(theta[2]), 0],
            [0, 0, 1],
        ]
    )
    R = np.dot(R_x, np.dot(R_y, R_z))
    return R


def isRotationMatrix(R):
    Rt = np.transpose(R)
    shouldBeIdentity = np.dot(Rt, R)
    I = np.identity(3, dtype=R.dtype)
    n = np.linalg.norm(I - shouldBeIdentity)
    return n < 1e-6


def rotationMatrixToEulerAnglesZYX(R):
    assert isRotationMatrix(R)

    if R[2, 0] < 1:
        if R[2, 0] > -1:
            y = np.arcsin(-R[2, 0])
            z = np.arctan2(R[1, 0], R[0, 0])
            x = np.arctan2(R[2, 1], R[1, 1])
        else:
            y = np.pi / 2
            z = -np.arctan2(-R[1, 2], R[1, 1])
            x = 0
    else:
        y = -np.pi / 2
        z = np.arctan2(-R[1, 2], R[1, 1])
        x = 0

    return np.array([x, y, z])


def rotationMatrixToEulerAnglesYZX(R):
    assert isRotationMatrix(R)

    if R[1, 0] < 1:
        if R[1, 0] > -1:
            z = np.arcsin(R[1, 0])
            y = np.arctan2(-R[2, 0], R[0, 0])
            x = np.arctan2(-R[1, 2], R[1, 1])
        else:
            z = -np.pi / 2
            y = -np.arctan2(-R[2, 1], R[2, 2])
            x = 0
    else:
        z = -np.pi / 2
        y = np.arctan2(R[2, 1], R[2, 2])
        x = 0

    return np.array([x, y, z])


def rotationMatrixToEulerAngles(R):
    assert isRotationMatrix(R)

    sy = math.sqrt(R[0, 0] * R[0, 0] + R[1, 0] * R[1, 0])

    singular = sy < 1e-6

    if not singular:
        x = math.atan2(R[2, 1], R[2, 2])
        y = math.atan2(-R[2, 0], sy)
        z = math.atan2(R[1, 0], R[0, 0])
    else:
        x = math.atan2(-R[1, 2], R[1, 1])
        y = math.atan2(-R[2, 0], sy)
        z = 0

    return np.array([x, y, z])