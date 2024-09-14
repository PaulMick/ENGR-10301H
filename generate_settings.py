import os
import cv2
import aruco_markers
import json

# settings JSON
settings = {
    "camera_settings": {
        "camera_name": str,
        "matrix_coefficients": list[list[float]],
        "distortion_coefficients": list[float]
    },
    "marker_settings": {
        "marker_family": str,
        "marker_length": float,
        "waypoint_markers": [],
        "marker_of_interest_id": int
    }
}

camera_name = cv2.VideoCapture(0).getBackendName()

settings["camera_settings"]["camera_name"] = camera_name

checkerboard_width = int(input("Checkerboard width (count): "))
checkerboard_height = int(input("Checkerboard height (count): "))
checkerboard_size = float(input("Checkerboard square size (mm): "))

print("Collecting calibration data, hold up checkerboard to camera")

os.system(f"aruco collect --width {checkerboard_width} --height {checkerboard_height} --squaresize {checkerboard_size}")

num_calibration_files = int(input("Num. files to use for calibration (40-80 reccommended): "))

os.system(f"aruco calibrate --cameraname {camera_name} --maxfiles {num_calibration_files}")

camera_settings = aruco_markers.load_camera_parameters(camera_name)

settings["camera_settings"]["matrix_coefficients"] = camera_settings[0].tolist()
settings["camera_settings"]["distortion_coefficients"] = camera_settings[1].tolist()[0]

marker_family = input("Marker Family (e.g. DICT_4X4_50): ")
assert marker_family in aruco_markers.ARUCO_DICT.keys()

settings["marker_settings"]["marker_family"] = marker_family

marker_length = float(input("Marker length (m): "))

settings["marker_settings"]["marker_length"] = marker_length

interest_id = int(input("ID of marker of interest (int): "))

settings["marker_settings"]["marker_of_interest_id"] = interest_id

num_waymarkers = int(input("Number of waypoint markers (int): "))

for i in range(1, num_waymarkers + 1):
    suffix = "th"
    if i % 10 == 1:
        suffix = "st"
    elif i % 10 == 2:
        suffix = "nd"
    elif i % 10 == 3:
        suffix = "rd"
    print(f"{i}{suffix} waypoint marker info (m and deg)")

    waymarker = {
        "id": int,
        "pose": {
            "x": float,
            "y": float,
            "z": float,
            "roll": float,
            "pitch": float,
            "yaw": float
        }
    }

    waymarker["id"] = int(input("ID (int): "))
    waymarker["pose"]["x"] = float(input("x: "))
    waymarker["pose"]["y"] = float(input("y: "))
    waymarker["pose"]["z"] = float(input("z: "))
    waymarker["pose"]["roll"] = float(input("roll: "))
    waymarker["pose"]["pitch"] = float(input("pitch: "))
    waymarker["pose"]["yaw"] = float(input("yaw: "))

    settings["marker_settings"]["waypoint_markers"].append(waymarker)

settings_file_name = input("Name of settings file: ")

out_file = open(f"settings\\{settings_file_name}.json", "w")
json.dump(settings, out_file, indent = 2)
out_file.close()
print(f"{settings_file_name}.json created successfully under ./settings!")