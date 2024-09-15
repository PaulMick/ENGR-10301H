import cv2
import cv2.aruco as aruco
import argparse
import json
import numpy as np

parser = argparse.ArgumentParser(description = "Tracks a single aruco marker with other markers as points of reference")
parser.add_argument("settings", help = "settings file to use for tracking")
args = parser.parse_args()

settings_file_name = args.settings
in_file = open(f"settings\\{settings_file_name}.json")

settings = json.load(in_file)

marker_length = settings["marker_settings"]["marker_length"]
matrix_coefs = np.matrix(settings["camera_settings"]["matrix_coefficients"])
distortion_coefs = np.matrix(settings["camera_settings"]["distortion_coefficients"])
valid_marker_ids = [settings["marker_settings"]["marker_of_interest_id"]]
for waymarker in settings["marker_settings"]["waypoint_markers"]:
    valid_marker_ids.append(waymarker["id"])

cam = cv2.VideoCapture(0)

aruco_dict = aruco.getPredefinedDictionary(0)
aruco_params = aruco.DetectorParameters()

def findArucoMarkers(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners, ids, rejected = aruco.detectMarkers(gray, aruco_dict, parameters = aruco_params)

    aruco.drawDetectedMarkers(frame, corners)

    return [corners, ids]

def estimateMarkerPoses(frame, corners, ids):
    pose_estimations = []
    if len(corners) > 0:
        for i in range(len(ids)):
            if not ids[i][0] in valid_marker_ids:
                continue
            rvec, tvec, marker_points = aruco.estimatePoseSingleMarkers(corners[i], marker_length, matrix_coefs, distortion_coefs)
            # print(f"rvec: {rvec}, tvec: {tvec}, marker_points: {marker_points}")
            print(f"[{(ids[i][0])}] Dist z: {tvec[0][0][2]}")
            pose_estimations.append({
                "id": int(ids[i][0]),
                "trans_vec": list(tvec[0][0]),
                "rot_vec": list(rvec[0][0])
            })
            cv2.drawFrameAxes(frame, matrix_coefs, distortion_coefs, rvec, tvec, marker_length)
    return pose_estimations

while True:
    ret, frame = cam.read()

    detections = findArucoMarkers(frame)
    marker_poses = estimateMarkerPoses(frame, detections[0], detections[1])
    # print(marker_poses)

    cv2.imshow("Feed", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cam.release()
cv2.destroyAllWindows()