import pose_solver
import numpy as np
from math import pi

marker_in_world_pose = [0, 0, 0, 0, 0, 0]
marker_in_cam_pose = [1, 5, -2, pi / 2, 0, 0]

cam_to_world_mat = pose_solver.get_cam_pose_rel_world(marker_in_cam_pose, marker_in_world_pose)

point = np.matrix([0, 0, 0, 1])

# print(point)

print(np.matmul(point, cam_to_world_mat))