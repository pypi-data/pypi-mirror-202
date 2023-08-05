import numpy as np
from matplotlib import cm
from porteratzolibs.visualization_o3d.open3d_utils import (
    convertcloud,
)
import copy

try:
    import open3d

    V3V = open3d.utility.Vector3dVector
    use_headless = False
except ImportError:
    use_headless = True


def check_point_format(nppoints):
    assert (
        (type(nppoints) == np.ndarray)
        or (type(nppoints) is list)
        or (type(nppoints) is tuple)
        or (type(nppoints) is o3d_pointSetClass)
    ), "Not valid point_cloud"

    if (type(nppoints) is not list) & (type(nppoints) is not tuple):
        if type(nppoints) is np.ndarray:
            if len(nppoints.shape) == 2:
                nppoints = [nppoints]
        if type(nppoints) is o3d_pointSetClass:
            nppoints = [nppoints]
    return nppoints


class pointSetClass:
    def __init__(self, points=None, color=[], persistant=False) -> None:
        self.colors = None
        self.points = None
        self.persistant = persistant
        self.updated = False
        if points is not None:
            self.update(points, color)

    def update(self, points, color=[]):
        self.points = points
        try:
            if len(np.asarray(color)) == len(self.points):
                if len(np.asarray(color).shape) == 2:
                    self.colors = color
                else:
                    color = color - np.min(color)
                    self.colors = cm.jet(color / np.max(color))[:, :3]
            elif len(color) > 0:
                self.colors = np.ones_like(points) * color
            self.updated = True
        except TypeError:
            pass
        except ValueError:
            pass

    def draw(self):
        pass

    def state_dict(self):
        if (self.persistant) or (self.updated):
            self.updated = False
            return {
                "points": self.points.astype(np.float32)
                if type(self.points) is np.ndarray
                else self.points,
                "colors": self.colors.astype(np.float32)
                if type(self.colors) is np.ndarray
                else self.colors,
            }
        else:
            return {}


class o3d_pointSetClass(pointSetClass):
    def __init__(self, points=None, color=[], persistant=False) -> None:
        self.cloud = None
        self.in_vis = False
        self.used_vis = None
        super().__init__(points, color, persistant)

    def update(self, points=[], color=[]):
        if len(points) > 0:
            super().update(points, color)
        if self.cloud is None:
            self.cloud = convertcloud(self.points)
        else:
            self.cloud.points = V3V(self.points)
        if self.colors is not None:
            self.cloud.colors = V3V(self.colors)
        self.updated = True

    def draw(self, vis):
        if (self.persistant) or (self.updated):
            if not self.in_vis:
                vis.add_geometry(self.cloud)
                self.in_vis = True
            else:
                vis.update_geometry(self.cloud)
            self.updated = False
        else:
            self.remove(vis)

    def remove(self, vis):
        vis.remove_geometry(self.cloud)
        self.in_vis = False

class multi_bounding_box:
    def __init__(self, workpoints, color) -> None:
        self.main_bb = open3d.geometry.OrientedBoundingBox.create_from_points(
            open3d.utility.Vector3dVector(workpoints)
        )
        self.main_bb.color = color
        self.scale_factor = 0.05
        self.number_of_lines = 8

        self.secondary_bb = []
        for i in range(self.number_of_lines):
            self.secondary_bb.append(copy.copy(self.main_bb))
            self.secondary_bb[-1].scale(
                1.0 + self.scale_factor + i * self.scale_factor,
                self.secondary_bb[-1].get_center(),
            )

    def set_points(self, workpoints):
        main_bb = open3d.geometry.OrientedBoundingBox.create_from_points(
            open3d.utility.Vector3dVector(workpoints)
        )
        self.main_bb.center = main_bb.center
        self.main_bb.extent = main_bb.extent
        self.main_bb.R = main_bb.R

        for n, i in enumerate(self.secondary_bb):
            sec = copy.copy(main_bb)
            sec.scale(1.0 + self.scale_factor + n * self.scale_factor, sec.get_center())
            i.center = sec.center
            i.extent = sec.extent
            i.R = sec.R

    def draw(self, vis):
        vis.add_geometry(self.main_bb)
        for i in self.secondary_bb:
            vis.add_geometry(i)

    def update(self, vis):
        vis.update_geometry(self.main_bb)
        for i in self.secondary_bb:
            vis.update_geometry(i)

    def remove(self, vis):
        vis.remove_geometry(self.main_bb)
        for i in self.secondary_bb:
            vis.remove_geometry(i)