# -*- coding: utf-8 -*-
from flask import Flask, render_template, Response, request
import cv2

app = Flask(__name__)
camera = cv2.VideoCapture(0)  # USB�J�����i/dev/video0�Ȃǁj

def gen_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# �F�؃`�F�b�N
def check_auth(username, password):
    return username == 'user' and password == 'pass'

# �F�ؗv��
def authenticate():
    return Response('Authentication required', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})

# ���ׂẴ��N�G�X�g�ɔF�؂�������
@app.before_request
def require_auth():
    auth = request.authorization
    if not auth or not check_auth(auth.username, auth.password):
        return authenticate()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
