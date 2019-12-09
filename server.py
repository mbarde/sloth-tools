from flask import escape
from flask import render_template
from flask import request
from flask import send_file
from flask import send_from_directory
from flask import Flask

import cv2
import os
import subprocess


def create_app():
    app = Flask(__name__,
                template_folder='/home/ubuntu/server',
                static_url_path='')

    import db
    db.init_app(app)

    @app.route('/')
    def index():
        return render_template('./index.html', title='Sloth Tools')

    @app.route('/nodes')
    def nodes():
        import db
        db = db.get_db()
        nodes = db.execute('SELECT * FROM node').fetchall()
        return render_template('./nodes.html', nodes=nodes)

    def sendCode(code, iterations):
        progPath = '/home/ubuntu/433Utils/RPi_utils/codesend'
        args = ['sudo', progPath, code]
        FNULL = open(os.devnull, 'w')
        for i in range(1, iterations):
            proc = subprocess.Popen(args, stdout=FNULL)
            proc.wait()
        return 'sent ({0}x): {1}'.format(escape(iterations), escape(code))

    def getNodeById(nodeId):
        import db
        db = db.get_db()
        node = db.execute('SELECT * FROM node WHERE id = ?', str(nodeId)).fetchone()
        return node

    def setNodeState(nodeId, state):
        import db
        db = db.get_db()
        db.execute('UPDATE node SET state = ? WHERE id = ?;', (state, nodeId))
        db.commit()

    @app.route('/on')
    def switchOn():
        nodeId = request.args.get('id')
        node = getNodeById(nodeId)
        res = sendCode(node['codeOn'], node['iterations'])
        if len(res) > 0:
            setNodeState(nodeId, 1)
        return res

    @app.route('/off')
    def switchOff():
        nodeId = request.args.get('id')
        node = getNodeById(nodeId)
        res = sendCode(node['codeOff'], node['iterations'])
        if len(res) > 0:
            setNodeState(nodeId, 0)
        return res

    @app.route('/webcam')
    def webcam():
        capture = cv2.VideoCapture(0)
        _, frame = capture.read()
        cv2.imwrite('webcam.jpg', frame)
        capture.release()
        return send_file('webcam.jpg', cache_timeout=-1)

    # node API
    @app.route('/node/create', methods=['GET', 'POST'])
    def nodeCreate():
        jsonData = request.get_json()
        if jsonData is not None:
            # do create
            return 'OK'
        node = {
            'title': '',
            'codeOn': '',
            'codeOff': '',
            'iterations': '3'
        }
        return render_template('./node.html', node=node, action='/node/create')

    @app.route('/node/read/<int:id>')
    def nodeRead(id):
        node = getNodeById(id)
        return dict(node)

    @app.route('/node/update/<int:id>', methods=['GET', 'POST'])
    def nodeUpdate(id):
        jsonData = request.get_json()
        if jsonData is not None:
            node = jsonData
            import db
            db = db.get_db()
            sql = 'UPDATE node SET title = ?, codeOn = ?, codeOff = ?, iterations = ? WHERE id = ?;'
            db.execute(
                sql,
                (node['title'], node['codeOn'], node['codeOff'],
                 node['iterations'], node['id'])
            )
            db.commit()
            return 'OK'
        node = getNodeById(id)
        actionUrl = '/node/update/{0}'.format(id)
        return render_template('./node.html', node=node, action=actionUrl)

    @app.route('/static/<path:path>')
    def sendStaticResources(path):
        return send_from_directory('static', path)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
