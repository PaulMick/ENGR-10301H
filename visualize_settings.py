import pose_solver
import numpy as np
from math import pi
import matplotlib.pyplot as plt
import json
import argparse

parser = argparse.ArgumentParser(description = "Tracks a single aruco marker with other markers as points of reference")
parser.add_argument("settings", help = "settings file to use for tracking")
args = parser.parse_args()

settings_file_name = args.settings
# in_file = open(f"/aruco/ENGR-10301H/settings/{settings_file_name}.json") # for linux
in_file = open(f"settings/{settings_file_name}.json") # for windows
settings = json.load(in_file)

def get_point(off_set_point: list[float], transform_mat: np.matrix) -> list[float]:
    off_set_point.append(1)
    out = np.matmul(off_set_point, transform_mat)
    return [float(out[0]), float(out[1]), float(out[2])]

def plot_axis(transform_mat: np.matrix, label: str):
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
    plot_3d.text(origin[0], origin[1], origin[2], label)

plot_3d = plt.axes(projection = "3d")

for waymarker in settings["marker_settings"]["waypoint_markers"]:
    waymarker_in_world_pose = [waymarker["pose"]["x"], waymarker["pose"]["y"], waymarker["pose"]["z"], waymarker["pose"]["rx"], waymarker["pose"]["ry"], waymarker["pose"]["rz"]]

    marker_to_world_mat = pose_solver.get_inverse_transformation_matrix(waymarker_in_world_pose)
    
    plot_axis(marker_to_world_mat, waymarker["id"])

plot_axis(np.identity(4), "World")

plot_3d.set_title("World View")
plot_3d.set_xlabel("X")
plot_3d.set_ylabel("Y")
plot_3d.set_zlabel("Z")
plot_3d.set_xlim3d(-5, 5)
plot_3d.set_ylim3d(-5, 5)
plot_3d.set_zlim3d(0, 10)

plt.show()