import pose_solver
import numpy as np
from math import pi
import matplotlib.pyplot as plt
import time

def get_point(off_set_point: list[float], transform_mat: np.matrix) -> list[float]:
    off_set_point.append(1)
    out = np.matmul(off_set_point, transform_mat)
    return [float(out[0]), float(out[1]), float(out[2])]

def plot_axis(transform_mat: np.matrix):
    origin = get_point([0, 0, 0], transform_mat)
    x_points = []
    x_points.append(origin)
    x_points.append(get_point([1, 0, 0], transform_mat))
    plot_3d.plot3D([p[0] for p in x_points], [p[1] for p in x_points], [p[2] for p in x_points], "red")
    y_points = []
    y_points.append(origin)
    y_points.append(get_point([0, 1, 0], transform_mat))
    plot_3d.plot3D([p[0] for p in y_points], [p[1] for p in y_points], [p[2] for p in y_points], "blue")
    z_points = []
    z_points.append(origin)
    z_points.append(get_point([0, 0, 1], transform_mat))
    plot_3d.plot3D([p[0] for p in z_points], [p[1] for p in z_points], [p[2] for p in z_points], "green")

plot_3d = plt.axes(projection = "3d")

marker_in_world_pose = [1, 2, 3, 0, 0, 0]
marker_in_cam_pose = [1, 5, -2, pi / 2, 0, 0]

marker_to_world_mat = pose_solver.get_inverse_transformation_matrix(marker_in_world_pose)
cam_to_world_mat = pose_solver.get_cam_pose_rel_world(marker_in_cam_pose, marker_in_world_pose)

point = np.matrix([0, 0, 0, 1])

world_point = np.matmul(point, cam_to_world_mat)

plot_axis(marker_to_world_mat)

plt.show()