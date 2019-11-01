from flask import escape
from flask import render_template
from flask import request
from flask import send_file
from flask import Flask

import cv2
import os
import subprocess

app = Flask(__name__, template_folder='/home/ubuntu/server')


@app.route('/')
def index():
    return render_template('./index.html')


@app.route('/send')
def sendcode():
    # calls C++
    code = request.args.get('code', '0')
    progPath = '/home/ubuntu/433Utils/RPi_utils/codesend'
    args = ['sudo', progPath, code]
    FNULL = open(os.devnull, 'w')
    proc = subprocess.Popen(args, stdout=FNULL)
    proc.wait()
    proc = subprocess.Popen(args, stdout=FNULL)
    proc.wait()
    proc = subprocess.Popen(args, stdout=FNULL)
    proc.wait()
    return f'send: {escape(code)}!'


@app.route('/webcam')
def webcam():
    capture = cv2.VideoCapture(0)
    _, frame = capture.read()
    cv2.imwrite('webcam.jpg', frame)
    capture.release()
    return send_file('webcam.jpg', cache_timeout=-1)
