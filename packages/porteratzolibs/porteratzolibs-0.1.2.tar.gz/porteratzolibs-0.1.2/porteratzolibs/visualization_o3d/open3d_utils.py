try:
    import open3d as o3d
    use_headless = False
except ImportError:
    use_headless = True
import numpy as np


def convertcloud(points):
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    return pcd


def downsample(point_cloud, leaf_size=0.005, return_idx=False):
    if return_idx:
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(point_cloud)
        _, rest, _ = pcd.voxel_down_sample_and_trace(
            voxel_size=leaf_size,
            min_bound=np.array([-10, -10, -10]),
            max_bound=np.array([10, 10, 10]),
        )
        return rest[rest != -1]
    else:
        return o3d.voxel_down_sample(point_cloud, leaf_size)