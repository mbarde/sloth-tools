from flask import escape
from flask import render_template
from flask import request
from flask import send_file
from flask import Flask

import cv2
import os
import subprocess


def create_app():
    app = Flask(__name__, template_folder='/home/ubuntu/server')

    @app.route('/')
    def index():
        nodes = [
           {'title': '📚 Bücherregal',
            'codeOn': '1361',
            'codeOff': '1364',
            },
           {'title': 'Wohnzimmer-Ecke',
            'codeOn': '5201',
            'codeOff': '5204',
            },
           {'title': 'Flur-Ecke',
            'codeOn': '4433',
            'codeOff': '4436',
            },
        ]
        return render_template('./index.html', nodes=nodes)

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

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
