
Full setup instructions

Required packages

Windows / Linux / RNX support

Run instructions

IP Webcam usage



---

📡 HandLaser (MediaPipe + OpenCV)

A real-time computer vision project that detects hands using MediaPipe and renders a neon laser prism effect between both hands using OpenCV.

It supports:

Android IP Webcam streaming

Linux (Debian / Ubuntu)

Windows

RNX Terminal Workspace (headless mode)



---

🚀 Features

✋ Real-time hand tracking (MediaPipe)

🌈 Neon rainbow laser prism effect

📡 IP Webcam Android support

🎥 Video recording output (MP4)

⚡ FPS + gesture HUD

🧠 Works without GUI (RNX mode supported)



---

📦 Requirements

Python Version

Python 3.8 – 3.11 recommended



---

🧰 Python Packages

Install all dependencies:

pip install opencv-python mediapipe numpy flask


---

🧩 System Dependencies (Linux / RNX)

Debian / Ubuntu / RNX

sudo apt update

sudo apt install -y \
libgl1 \
libglib2.0-0 \
libsm6 \
libxext6 \
libxrender1 \
ffmpeg \
v4l-utils


---

🪟 Windows Setup

Install Python packages:

pip install opencv-python mediapipe numpy flask

If camera issues occur:

Install Microsoft Visual C++ Redistributable

Ensure webcam is not used by another app



---

📱 Android IP Webcam Setup

Install on Android:

IP Webcam (Play Store)


Start server and copy URL:

http://YOUR_PHONE_IP:8080/video

Example:

http://192.168.3.10:8080/video


---

📁 Project Files

maincam.py          # Main laser prism application
cam-test.py      # Camera test script
preview.py       # Optional Flask preview server
README.md        # Documentation


---

▶️ How to Run

🐧 Linux / RNX

Run maincam project:

python3 maincam.py

Run camera test:

python3 cam-test.py


---

🪟 Windows

python maincam.py


---

📡 RNX Mode (No GUI Support)

If cv2.imshow() does not work:

The program automatically runs headless

Output saved as MP4


Run:

python3 maincam.py

Then check:

hand_laser_output.mp4


---

📱 Using IP Webcam (Required for RNX / Android Linux)

Edit inside maincam.py:

IP_CAM_URL = "http://192.168.3.10:8080/video"

Make sure:

Phone + device are on same WiFi

URL opens in browser before running script



---

🎥 Output

The program generates:

hand_laser_output.mp4

Includes:

Hand tracking skeleton

Neon rainbow beams

Prism effect between both hands

FPS + gesture overlay



---

⚠️ Troubleshooting

❌ Camera not opening

Check IP Webcam URL

Try /video, /videofeed, or /shot.jpg



---

❌ Qt / xcb error (RNX/Linux)

Fix:

sudo apt install libxcb-xinerama0

OR use headless mode (recommended):

Remove cv2.imshow()



---

❌ No video output

Ensure:

out.write(frame) is running

Correct resolution matches camera input



---

❌ MediaPipe error

Reinstall:

pip install mediapipe --upgrade


---

🧠 Architecture

Android Camera (IP Webcam)
        ↓
OpenCV Video Stream
        ↓
MediaPipe Hands Detection
        ↓
Laser Prism Renderer
        ↓
MP4 Video Output


---

💡 Future Improvements

Real-time browser streaming (Flask Web UI)

Gesture-based color switching

3D depth simulation

Multi-user hand tracking

AI smoothing filter



---

👨‍💻 Author

OEDX Digitals


