import numpy as np
import math

"""
IMPORTANT!!
poses in the form: [x, y, z, rx, ry, rx]
translation vectors in the form: [x, y, z]
rotation vectors in the form: [rx, ry, rz]
"""

# 3D translation vector to 3D translation transformation matrix
def get_trans_matrix(trans_vec: list[float]) -> np.matrix:
    mat = np.identity(4)
    mat[3, 0] = -trans_vec[0]
    mat[3, 1] = -trans_vec[1]
    mat[3, 2] = -trans_vec[2]
    return mat

# 3D rotation vector to 3D rotation transformation matrix
def get_rot_matrix(rot_vec: list[float]) -> np.matrix:
    x_mat = np.identity(4)
    x_mat[1, 1] = math.cos(rot_vec[0])
    x_mat[1, 2] = math.sin(rot_vec[0])
    x_mat[2, 2] = math.cos(rot_vec[0])
    x_mat[2, 1] = -math.sin(rot_vec[0])

    y_mat = np.identity(4)
    y_mat[0, 0] = math.cos(rot_vec[1])
    y_mat[2, 0] = math.sin(rot_vec[1])
    y_mat[2, 2] = math.cos(rot_vec[1])
    y_mat[0, 2] = -math.sin(rot_vec[1])

    z_mat = np.identity(4)
    z_mat[0, 0] = math.cos(rot_vec[2])
    z_mat[0, 1] = math.sin(rot_vec[2])
    z_mat[1, 1] = math.cos(rot_vec[2])
    z_mat[1, 0] = -math.sin(rot_vec[2])

    return np.matmul(np.matmul(x_mat, y_mat), z_mat)

# 3D pose to 3D transformation matrix
def get_transformation_matrix(pose: list[float]) -> np.matrix:
    return np.matmul(get_trans_matrix(pose[:3:]), get_rot_matrix(pose[3:6:]))

# 3D pose to inverse of the 3D transformation matrix
def get_inverse_transformation_matrix(pose: list[float]) -> np.matrix:
    return np.linalg.inv(np.matmul(get_trans_matrix(pose[:3:]), get_rot_matrix(pose[3:6:])))

# Calculate 3D transformation matrix to convert camera space to world space
def get_cam_to_world_transform(marker_in_cam_pose: list[float], marker_in_world_pose: list[float]) -> np.matrix:
    marker_to_world_mat = get_inverse_transformation_matrix(marker_in_world_pose)
    cam_to_marker_mat = get_transformation_matrix(marker_in_cam_pose)
    cam_to_world_mat = np.matmul(cam_to_marker_mat, marker_to_world_mat)
    return cam_to_world_mat

# 3D translation vector of marker in world space
def get_marker_pos_rel_world(marker_in_cam_pose: list[float], cam_to_world_mat: np.matrix) -> list[float]:
    marker_to_cam_mat = get_inverse_transformation_matrix(marker_in_cam_pose)
    marker_to_world_mat = np.matmul(marker_to_cam_mat, cam_to_world_mat)
    return list(np.matmul([0, 0, 0, 1], marker_to_world_mat))

"""
From:
{
    "trans_vec": [x, y, z],
    "rot_vec": [rx, ry, rz]
}
To:
[x, y, z, rx, ry, rz]
"""
def get_vec_pose_as_list(pose: dict) -> list[float]:
    return [pose["trans_vec"][0], pose["trans_vec"][1], pose["trans_vec"][2], pose["rot_vec"][0], pose["rot_vec"][1], pose["rot_vec"][2]]

"""
From:
{
    "x": x,
    "y": y,
    "z": z,
    "rx": rx,
    "ry": ry,
    "rz": rz,
}
To:
[x, y, z, rx, ry, rz]
"""
def get_dict_pose_as_list(pose: dict) -> list[float]:
    return [pose["x"], pose["y"], pose["z"], pose["rx"], pose["ry"], pose["rz"]]