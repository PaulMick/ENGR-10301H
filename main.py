import cv2
import cv2.aruco as aruco
import argparse
import json
import numpy as np
import statistics as stats
import pose_solver
import platform

parser = argparse.ArgumentParser(description = "Tracks a single aruco marker with other markers as points of reference")
parser.add_argument("settings", help = "settings file to use for tracking")
args = parser.parse_args()

# Name of JSON settings file
settings_file_name = args.settings

if platform.system() == "Windows":
    in_file = open(f"settings/{settings_file_name}.json")
elif platform.system() == "Linux":
    in_file = open(f"/aruco/ENGR-10301H/settings/{settings_file_name}.json")
else:
    print("Unrecognized OS")
    exit(1)

# JSON settings file
settings = json.load(in_file)

# Parsing marker information
marker_length = settings["marker_settings"]["marker_length"]
matrix_coefs = np.matrix(settings["camera_settings"]["matrix_coefficients"])
distortion_coefs = np.matrix(settings["camera_settings"]["distortion_coefficients"])
valid_marker_ids = [settings["marker_settings"]["marker_of_interest_id"]]
active_marker_id = settings["marker_settings"]["marker_of_interest_id"]
waymarker_ids = []
waymarker_world_poses = {}
for waymarker in settings["marker_settings"]["waypoint_markers"]:
    valid_marker_ids.append(waymarker["id"])
    waymarker_ids.append(waymarker["id"])
    waymarker_world_poses[waymarker["id"]] = waymarker["pose"]

cam = cv2.VideoCapture(0)

aruco_dict = aruco.getPredefinedDictionary(0)
aruco_params = aruco.DetectorParameters()

# Finds corners and ids of aruco markers in frame
def findArucoMarkers(frame) -> list[list]:
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners, ids, rejected = aruco.detectMarkers(gray, aruco_dict, parameters = aruco_params)

    aruco.drawDetectedMarkers(frame, corners)

    return [corners, ids]

# Estimates poses in camera space in frame
def estimateMarkerPoses(frame, corners, ids) -> list[dict]:
    pose_estimations = []
    if len(corners) > 0:
        for i in range(len(ids)):
            # Reject invalid ids
            if not ids[i][0] in valid_marker_ids:
                print(f"Invalid tag ID: {ids[i][0]}")
                continue
            rvec, tvec, marker_points = aruco.estimatePoseSingleMarkers(corners[i], marker_length, matrix_coefs, distortion_coefs)
            pose_estimations.append({
                "id": int(ids[i][0]),
                "trans_vec": list(tvec[0][0]),
                "rot_vec": list(rvec[0][0])
            })
            cv2.drawFrameAxes(frame, matrix_coefs, distortion_coefs, rvec, tvec, marker_length)
    return pose_estimations

def main():
    # Camera location calibration
    data_points = []

    # Calibration phase: figures out where camera is in world space
    while len(data_points) < 1000:
        ret, frame = cam.read()

        detections = findArucoMarkers(frame)
        marker_poses = estimateMarkerPoses(frame, detections[0], detections[1])

        waymarker_poses = [pose for pose in marker_poses if pose["id"] in waymarker_ids]
        # print(waymarker_poses)

        cam_poses = []
        for p in waymarker_poses:
            marker_in_world_pose = pose_solver.get_dict_pose_as_list(waymarker_world_poses[p["id"]])
            cam_poses.append(list(np.matmul([0, 0, 0, 1], pose_solver.get_cam_to_world_transform(pose_solver.get_vec_pose_as_list(p), marker_in_world_pose))))
        # print(cam_poses)

        if len(cam_poses) > 0:
            avg_cam_pose = [[stats.mean([pose[i] for pose in cam_poses]) for i in range(3)]]
            # print(avg_cam_pose)

            data_points.append(avg_cam_pose)

        cv2.imshow("Calibration Feed", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cv2.destroyAllWindows()

    # print(data_points)
    cam_in_world_pose = [[stats.mean([pose[0][i] for pose in data_points]) for i in range(3)]]
    print(cam_in_world_pose)

    # Active tracking: tracks marker of interest in world space
    while True:
        ret, frame = cam.read()

        detections = findArucoMarkers(frame)
        marker_poses = estimateMarkerPoses(frame, detections[0], detections[1])

        cv2.imshow("Active Tracking Feed", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()