import time
import numpy as np
import matplotlib.pyplot as plt
import cv2
from flask import Flask, Response


app = Flask(__name__)
@app.route("/")
def hello_world():
    return """
    <body style="background: black;">
        <div style="width: 240px; margin: 0px auto;">
            <img src="/mjpeg" />
        </div>
    </body>
    """
# setup camera and resolution
cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
def gather_img():
    while True:
        time.sleep(0.1)
        _, img = cam.read()
        _, frame = cv2.imencode('.jpg', img)
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame.tobytes() + b'\r\n')
@app.route("/mjpeg")
def mjpeg():
    return Response(gather_img(), mimetype='multipart/x-mixed-replace; boundary=frame')
app.run(host='0.0.0.0', port=8123, threaded=True)