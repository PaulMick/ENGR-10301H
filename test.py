import pose_solver

marker_in_world_pose = [0, 1, 2, 0, 0, 0]
marker_in_cam_pose = [1, 1, 1, 0, 0, 0]

print(pose_solver.get_cam_pose_rel_world(marker_in_cam_pose, marker_in_world_pose))
