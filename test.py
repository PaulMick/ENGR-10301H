import statistics as stats

cam_poses = [[1, 1, 1, 1], [0, 0, 0, 1]]

out = [[stats.mean([pose[i] for pose in cam_poses]) for i in range(3)]]

print(out)