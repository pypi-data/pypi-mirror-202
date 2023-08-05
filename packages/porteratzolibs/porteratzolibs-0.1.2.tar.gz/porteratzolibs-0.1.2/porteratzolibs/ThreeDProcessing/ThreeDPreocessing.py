import numpy as np
import pclpy
import open3d as o3d
from porteratzolibs.ThreeDProcessing import pclpy_utils 
from porteratzolibs.tictoc import bench_dict


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
        return pclpy_utils.voxelize(point_cloud, leaf_size)


def outliers(points, min_n=6, radius=0.4, organized=True):
    _points = pclpy_utils.radius_outlier_removal(points, min_n, radius, organized)
    return _points[~np.all(np.isnan(_points), axis=1)]


def farthest_point_sample(xyz, npoint):
    N, _ = xyz.shape
    centroids = []
    distance = np.ones(N) * 1e10
    farthest = np.random.randint(0, N)
    for i in range(npoint):
        centroids.append(farthest)
        centroid = xyz[farthest, :]
        dist = np.sum((xyz - centroid) ** 2, -1)
        mask = dist < distance
        distance[mask] = dist[mask]
        farthest = int(np.where(distance == np.max(distance))[0][0])
    return centroids


def normal_filter(
        subject_cloud,
        search_radius=0.05,
        verticality_threshold=0.3,
        curvature_threshold=0.3,
        return_indexes=False,
):
    bench_dict["normals"].gstep()
    non_ground_normals = pclpy_utils.extract_normals(subject_cloud, search_radius)
    bench_dict["normals"].step("extract")
    # remove Nan points
    non_nan_mask = np.bitwise_not(np.isnan(non_ground_normals.normals[:, 0]))
    non_nan_cloud = subject_cloud[non_nan_mask]
    non_nan_normals = non_ground_normals.normals[non_nan_mask]
    non_nan_curvature = non_ground_normals.curvature[non_nan_mask]
    bench_dict["normals"].step("nan")

    # get mask by filtering verticality and curvature
    verticality = np.dot(non_nan_normals, [[0], [0], [1]])
    verticality_mask = (verticality < verticality_threshold) & (
            -verticality_threshold < verticality
    )
    curvature_mask = non_nan_curvature < curvature_threshold
    verticality_curvature_mask = verticality_mask.ravel() & curvature_mask.ravel()

    only_horizontal_points = non_nan_cloud[verticality_curvature_mask]
    bench_dict["normals"].step("filter")
    bench_dict["normals"].gstop()

    if return_indexes:
        out_index = non_nan_mask
        out_index[non_nan_mask] = verticality_curvature_mask
        return out_index
    else:
        return only_horizontal_points


def seg_normals(
        filtered_points,
        search_radius=0.05,
        normalweight=0.01,
        miter=1000,
        distance=0.01,
        rlim=[0, 0.2],
):
    indices, model = pclpy_utils.segment_normals(
        filtered_points,
        search_radius=search_radius,
        model=pclpy.pcl.sample_consensus.SACMODEL_CYLINDER,
        method=pclpy.pcl.sample_consensus.SAC_RANSAC,
        normalweight=normalweight,
        miter=miter,
        distance=distance,
        rlim=rlim,
    )
    return indices, model
    