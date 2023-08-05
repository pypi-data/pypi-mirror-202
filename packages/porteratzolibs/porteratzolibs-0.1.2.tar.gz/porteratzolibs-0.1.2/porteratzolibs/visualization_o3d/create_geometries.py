import numpy as np
from porteratzolibs.geometry import rotation_matrix_from_vectors

def make_plane(coefs, center=[0, 0, 0]):
    ll, ul = -1, 1
    step = (ul - ll) / 10
    planepoints = np.meshgrid(np.arange(ll, ul, step), np.arange(ll, ul, step))
    plane = np.array(
        [
            planepoints[0].flatten(),
            planepoints[1].flatten(),
            np.zeros(len(planepoints[0].flatten())),
        ]
    ).T
    R = rotation_matrix_from_vectors([0, 0, 1], coefs[0:3])
    return np.add(np.matmul(R, plane.T).T, center)

def make_pointvector(coefs, centroid=[0, 0, 0], length=1, dense=10):
    assert len(coefs) == 3, "Need x,y,z normalvector"
    newcoefs = np.array(coefs) / np.linalg.norm(np.array(coefs))
    pointline = np.arange(
        length / dense, length + length / dense, length / dense
    )
    pointline = np.vstack([pointline, pointline, pointline])
    out = np.add(np.multiply(pointline.T, newcoefs), centroid)
    return out

def make_sphere(centroid=[0, 0, 0], radius=1, dense=90):
    n = np.arange(0, 360, int(360 / dense))
    n = np.deg2rad(n)
    x, y = np.meshgrid(n, n)
    x = x.flatten()
    y = y.flatten()
    sphere = np.vstack(
        [
            centroid[0] + np.sin(x) * np.cos(y) * radius,
            centroid[1] + np.sin(x) * np.sin(y) * radius,
            centroid[2] + np.cos(x) * radius,
        ]
    ).T
    return sphere

def make_cylinder(model=[0, 0, 0, 1, 0, 0, 1], length=1, dense=10):
    radius = model[6]
    X, Y, Z = model[:3]
    direction = model[3:6] / np.linalg.norm(model[3:6])
    n = np.arange(0, 360, int(360 / dense))
    height = np.arange(0, length, length / dense)
    n = np.deg2rad(n)
    x, z = np.meshgrid(n, height)
    x = x.flatten()
    z = z.flatten()
    cyl = np.vstack([np.cos(x) * radius, np.sin(x) * radius, z]).T
    rotation = rotation_matrix_from_vectors([0, 0, 1], model[3:6])
    rotatedcyl = np.matmul(rotation, cyl.T).T + np.array([X, Y, Z])
    return rotatedcyl