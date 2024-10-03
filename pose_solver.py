import numpy as np
import math

"""
IMPORTANT!!
poses in the form: [x, y, z, rx, ry, rx]
translation vectors in the form: [x, y, z]
rotation vectors in the form: [rx, ry, rz]
"""

def get_trans_matrix(x: float, y: float, z: float) -> np.matrix:
    mat = np.identity(4)
    mat[3, 0] = x
    mat[3, 1] = y
    mat[3, 2] = z
    return mat

def get_rot_matrix(rx: float, ry: float, rz: float) -> np.matrix:
    x_mat = np.identity(4)
    x_mat[1, 1] = math.cos(rx)
    x_mat[1, 2] = math.sin(rx)
    x_mat[2, 1] = math.cos(rx)
    x_mat[2, 2] = -math.sin(rx)

    y_mat = np.identity(4)
    y_mat[0, 0] = math.cos(ry)
    y_mat[2, 0] = math.sin(ry)
    y_mat[2, 2] = math.cos(ry)
    y_mat[0, 2] = -math.sin(ry)

    z_mat = np.identity(4)
    z_mat[0, 0] = math.cos(rz)
    z_mat[0, 1] = math.sin(rz)
    z_mat[1, 1] = math.cos(rz)
    z_mat[1, 0] = -math.sin(rz)

    return np.matmul(np.matmul(x_mat, y_mat), z_mat)

def get_trans_matrix(trans_vec: list[float]) -> np.matrix:
    mat = np.identity(4)
    mat[3, 0] = trans_vec[0]
    mat[3, 1] = trans_vec[1]
    mat[3, 2] = trans_vec[2]
    return mat

def get_rot_matrix(rot_vec: list[float]) -> np.matrix:
    x_mat = np.identity(4)
    x_mat[1, 1] = math.cos(rot_vec[0])
    x_mat[1, 2] = math.sin(rot_vec[0])
    x_mat[2, 1] = math.cos(rot_vec[0])
    x_mat[2, 2] = -math.sin(rot_vec[0])

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

def get_camera_pose_rel_world(marker_in_cam_pose: list[float], marker_in_world_pose: list[float]) -> list[float]:
    pass

def get_marker_pos_rel_world(marker_in_cam_pose: list[float], cam_in_world_pose: list[float]) -> list[float]:
    pass