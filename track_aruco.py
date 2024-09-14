import cv2
import cv2.aruco as aruco
import argparse

# parser = argparse.ArgumentParser(description = "Tracks a single aruco marker with other markers as points of reference")
# parser.add_argument("")

cam = cv2.VideoCapture(0)

def findArucoMarkers(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
    aruco_params = aruco.DetectorParameters()
    corners, ids, rejected = aruco.detectMarkers(gray, aruco_dict, parameters = aruco_params)
    print(ids)
    aruco.drawDetectedMarkers(frame, corners)
    return [corners, ids]

# def estimateMarkerPoses(frame, corners, ids, matrix_coefs, distortion_coefs):
#     aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
#     aruco_params = aruco.DetectorParameters()
#     if len(corners) > 0:
#         for i in range(len(ids)):
#             rvec, tvec, marker_points = aruco.estimatePoseSingleMarkers(corners[i], )

while True:
    ret, frame = cam.read()

    detections = findArucoMarkers(frame)

    cv2.imshow("Feed", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cam.release()
cv2.destroyAllWindows()