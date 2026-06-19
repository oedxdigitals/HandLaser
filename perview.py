from flask import Flask, Response
import cv2

app = Flask(__name__)

cap = cv2.VideoCapture(
    "http://192.168.3.10:8080/video"
)


def generate():

    while True:

        ret, frame = cap.read()

        if not ret:
            continue


        _, jpg = cv2.imencode('.jpg', frame)

        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n'
            +
            jpg.tobytes()
            +
            b'\r\n'
        )


@app.route('/')

def video():

    return Response(

        generate(),

        mimetype='multipart/x-mixed-replace; boundary=frame'

    )


app.run(

    host='0.0.0.0',

    port=5000

)

