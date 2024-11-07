import pose_solver
import math

marker_in_camera_pose = [0, 0, 1, 0, 0, 0]
marker_in_world_pose = [0, 0, 0, 0, 0, 0]

transform = pose_solver.get_cam_to_world_transform(marker_in_camera_pose, marker_in_world_pose)

camera_in_world_pose = pose_solver.get_pose_from_transform(transform)

print(camera_in_world_pose)