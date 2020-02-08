from flask import escape
from flask import render_template
from flask import request
from flask import send_from_directory
from flask import Flask
from service import CRUDService
from utils import bits2int
from utils import int2bits

import os
import subprocess


def create_app():
    # absolute path to the codesend binary
    # from https://github.com/ninjablocks/433Utils
    codesendBinPath = '/home/ubuntu/433Utils/RPi_utils/codesend'

    app = Flask(__name__,
                template_folder='.',
                static_url_path='')

    import db
    db.init_app(app)

    @app.route('/')
    def index():
        return render_template('./index.html', title='Sloth Tools')

    def sendCode(code, iterations):
        if not os.path.isfile(codesendBinPath):
            return 'codesend binary not found'
        args = ['sudo', codesendBinPath, code]
        FNULL = open(os.devnull, 'w')
        for i in range(1, iterations):
            proc = subprocess.Popen(args, stdout=FNULL)
            proc.wait()
        return 'sent ({0}x): {1}'.format(escape(iterations), escape(code))

    def setNodeState(nodeId, state):
        import db
        db = db.get_db()
        db.execute('UPDATE node SET state = ? WHERE id = ?;', (state, nodeId))
        db.commit()

    @app.route('/on')
    def switchOn():
        nodeId = request.args.get('id')
        nodeService = CRUDService('node')

        if nodeId is None:
            res = ''
            nodes = nodeService.read()
            for node in nodes:
                nodeRes = sendCode(node['codeOn'], node['iterations'])
                if len(nodeRes) > 0:
                    setNodeState(node['id'], 1)
                res += nodeRes + '<br/>'
        else:
            node = nodeService.read(nodeId)
            res = sendCode(node['codeOn'], node['iterations'])
            if len(res) > 0:
                setNodeState(node['id'], 1)

        return res

    @app.route('/off')
    def switchOff():
        nodeId = request.args.get('id')
        nodeService = CRUDService('node')

        if nodeId is None:
            res = ''
            nodes = nodeService.read()
            for node in nodes:
                nodeRes = sendCode(node['codeOff'], node['iterations'])
                if len(nodeRes) > 0:
                    setNodeState(node['id'], 0)
                res += nodeRes + '<br/>'
        else:
            node = nodeService.read(nodeId)
            res = sendCode(node['codeOff'], node['iterations'])
            if len(res) > 0:
                setNodeState(node['id'], 0)

        return res

    # node API
    @app.route('/nodes')
    def nodes():
        nodeService = CRUDService('node')
        nodes = nodeService.read()
        return render_template('./nodes.html', nodes=nodes)

    @app.route('/node/create', methods=['GET', 'POST'])
    def nodeCreate():
        nodeService = CRUDService('node')

        node = None
        jsonData = request.get_json()

        if jsonData is not None:
            node = jsonData
            if nodeService.create(node):
                return 'OK'

        if node is None:
            node = nodeService.getEmpty()
            node['iterations'] = '3'

        return render_template(
            './node.html', node=node,
            action='/node/create', method='POST',
            title='Add node', submitLabel='Create')

    @app.route('/node/read/<int:id>', methods=['GET'])
    def nodeRead(id):
        nodeService = CRUDService('node')
        node = nodeService.read(id)
        return dict(node)

    @app.route('/node/update/<int:id>', methods=['GET', 'POST'])
    def nodeUpdate(id):
        node = None
        nodeService = CRUDService('node')

        jsonData = request.get_json()
        if jsonData is not None:
            node = jsonData
            if nodeService.update(node):
                return 'OK'

        if node is None:
            node = nodeService.read(id)

        actionUrl = '/node/update/{0}'.format(id)
        return render_template(
            './node.html', node=node,
            action=actionUrl, method='POST',
            title='Update node', submitLabel='Update')

    @app.route('/node/delete/<int:id>', methods=['DELETE'])
    def nodeDelete(id):
        nodeService = CRUDService('node')
        nodeService.delete(id)
        return 'OK'

    # event API
    @app.route('/event/create', methods=['GET', 'POST'])
    def eventCreate():
        eventService = CRUDService('event')

        event = None
        jsonData = request.get_json()

        if jsonData is not None:
            event = jsonData
            if eventService.create(event):
                return 'OK'

        if event is None:
            event = eventService.getEmpty()
            event['weekdays'] = bits2int([] * 7)  # all day
            event['hour'] = 12
            event['minute'] = 0

        return render_template(
            './event.html', event=event,
            action='/event/create', method='POST',
            title='Add event', submitLabel='Create')

    @app.route('/event/read/<int:id>', methods=['GET'])
    def eventRead(id):
        eventService = CRUDService('event')
        event = eventService.read(id)
        return dict(event)

    @app.route('/event/bynode/<int:nodeIdRef>', methods=['GET'])
    def eventReadByNode(nodeIdRef):
        eventService = CRUDService('event')
        events = eventService.readBy('nodeIdRef', nodeIdRef)
        return render_template('./events.html', events=events)

    @app.route('/event/update/<int:id>', methods=['GET', 'POST'])
    def eventUpdate(id):
        event = None
        eventService = CRUDService('event')

        jsonData = request.get_json()
        if jsonData is not None:
            event = jsonData
            if eventService.update(event):
                return 'OK'

        if event is None:
            event = eventService.read(id)

        actionUrl = '/event/update/{0}'.format(id)
        return render_template(
            './event.html', event=event,
            action=actionUrl, method='POST',
            title='Update event', submitLabel='Update')

    @app.route('/event/delete/<int:id>', methods=['DELETE'])
    def eventDelete(id):
        eventService = CRUDService('event')
        eventService.delete(id)
        return 'OK'

    @app.route('/static/<path:path>')
    def sendStaticResources(path):
        return send_from_directory('static', path)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
