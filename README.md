# ENGR-10301H ArUco Marker Tracking System

This respository is for my ENGR-10301H class project codebase.

This README will serve as instructions for how to setup and use my system to track an object of interest with ArUco markers on a Raspbian system with an attached camera.

# Setup

## Raspberry Pi Configuration

Set up the Raspberry Pi with Raspberry Pi OS (64-bit) by follow [these instructions.](https://www.raspberrypi.com/documentation/computers/getting-started.html)

After booting the Raspberry Pi and connecting to it (either directly with monitor/keyboard/mouse, or via SSH), we need to change some configuration settings to make the camera module work.

Navigate to the `/boot/config.txt` file. Inside, make sure the following settings are set accordingly:
```
start_x=1
...
gpu_mem=128
```

And that the following line is commented out:
```
#camera_auto_detect=1
```

Now, making sure the camera module is connected, reboot the Raspberry Pi for the changes to take effect.

Create the project directory:
```
sudo mkdir /aruco
sudo chmod 777 /aruco
```

Clone this repository (you will need to connect the Pi to the internet, either by ethernet or WiFi):
```
cd /aruco
git clone https://github.com/PaulMick/ENGR-10301H.git
cd ENGR-10301H
```

Set up the python virtual environment:
```
python -m venv tracking-env
source tracking-env/bin/activate
python -m pip install --upgrade pip
pip install-r requirements.txt
```

# Field Tracking Setup

##

# Settings Creation

You will need a flat checkerboard to calibrate the camera. I recommend printing out `camera-calibration-checker-board_9x7.pdf` and taping it to a flat surface (cardboard, clipboard, etc.).

![Calibration Checkerboard](images/Checkerboard.png)

Run the calibration and settings generation script:
```
python generate_settings.py
```

## Camera Calibration

If the camera has not been calibrated, enter "`y`" when asked whether to calibrate camera.

Enter the width, height, and square size (mm) of the calibration checkerboard (recommended one is width 9, height 7, square size 20).

In the camera feed that popped up, moved the checkboard around at different distances and orientations for around 30 seconds, ensuring that the colorful dots are still being drawn in the feed. Press ESC to end the feed.

Enter a number of pictures to be used for camera calibration (recommended 50-60, more takes much longer). Give it time to process.

Next, enter the family of ArUco markers that is going to be used for tracking (recommended is "`DICT_4X4_50`").

Enter the marker length in meters (recommended 0.05).

Enter the ID of the marker of interest. This is the marker that will be attached to the robot to be tracked.

Enter the number of other waypoint markers. These are the marker(s) that will be in set locations around the field. For each waypoint marker, you will need to enter that waypoint marker's x, y, and x offset to the world's origin (all in meters), as well as the waypoints marker's rotations about the x, y, and z axiis.

After entering all of the waypoint marker information, provide a name for the settings file. Be sure to NOT include "`.json`" at the end, only the name (e.x. "`test-settings`").

The new settings file should be created under `./settings`.

Credits/Sources/Resources:
[https://forums.raspberrypi.com/viewtopic.php?t=331441](https://forums.raspberrypi.com/viewtopic.php?t=331441)
