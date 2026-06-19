import cv2

URL = "http://192.168.3.10:8080/video"

cap = cv2.VideoCapture(URL)

if not cap.isOpened():
    print("Cannot connect")
    exit()

print("Connected!")

while True:
    ret, frame = cap.read()

    if not ret:
        print("No frame")
        continue

    cv2.imshow("IP Webcam", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
