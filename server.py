from collections import OrderedDict
from events import EventTable
from flask import escape
from flask import render_template
from flask import request
from flask import send_from_directory
from flask import Flask
from service import CRUDService
from utils import bits2int
from utils import getWeekdays
from utils import int2bits
from utils import sqlrow2dict
from utils import weekdays2bits

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

    def switchNode(nodeId, state):
        nodeService = CRUDService('node')
        stateStr = 'codeOn'
        if state == 0:
            stateStr = 'codeOff'

        node = nodeService.read(nodeId)
        res = sendCode(node[stateStr], node['iterations'])
        if len(res) > 0:
            setNodeState(node['id'], state)

        return res

    @app.route('/on')
    def switchOn():
        nodeId = request.args.get('id')

        if nodeId is None:
            res = ''
            nodeService = CRUDService('node')
            nodes = nodeService.read()
            for node in nodes:
                nodeRes = switchNode(node['id'], 1)
                res += nodeRes + '<br/>'
        else:
            res = switchNode(nodeId, 1)

        return res

    @app.route('/off')
    def switchOff():
        nodeId = request.args.get('id')

        if nodeId is None:
            res = ''
            nodeService = CRUDService('node')
            nodes = nodeService.read()
            for node in nodes:
                nodeRes = switchNode(node['id'], 0)
                res += nodeRes + '<br/>'
        else:
            res = switchNode(nodeId, 0)

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
    @app.route('/event/create/<int:nodeId>', methods=['GET', 'POST'])
    def eventCreate(nodeId):
        eventService = CRUDService('event')

        event = None
        jsonData = request.get_json()

        if jsonData is not None:
            event = jsonData
            event['nodeIdRef'] = nodeId

            if event['switchOn'] == 'True':
                event['switchOn'] = True
            else:
                event['switchOn'] = False

            bits = weekdays2bits(event)
            event['weekdays'] = bits2int(bits)

            if eventService.create(event):
                eventTable.loadFromDB()
                return 'OK'

        if event is None:
            event = eventService.getEmpty()
            event['weekdays'] = bits2int([] * 7)  # all day
            event['hour'] = 12
            event['minute'] = 0

        nodeService = CRUDService('node')
        node = nodeService.read(nodeId)

        return render_template(
            './event.html', event=event, node=node,
            action='/event/create/' + str(nodeId), method='POST',
            title='Add event for ' + node['title'], submitLabel='Create')

    @app.route('/event/read/<int:id>', methods=['GET'])
    def eventRead(id):
        eventService = CRUDService('event')
        event = eventService.read(id)
        return dict(event)

    @app.route('/event/bynode/<int:nodeId>', methods=['GET'])
    def eventReadByNode(nodeId):
        eventService = CRUDService('event')
        rows = eventService.readBy('nodeIdRef', nodeId)

        events = []
        for row in rows:
            event = sqlrow2dict(row)

            event['hour'] = str(event['hour']).zfill(2)
            event['minute'] = str(event['minute']).zfill(2)

            if event['switchOn'] == 0:
                event['switchOn'] = 'off'
            else:
                event['switchOn'] = 'on'

            bits = int2bits(event['weekdays'])
            event['weekdays'] = OrderedDict()
            days = getWeekdays()
            i = 0
            for day in days:
                event['weekdays'][day] = bits[i]
                i += 1

            events.append(event)

        nodeService = CRUDService('node')
        node = nodeService.read(nodeId)

        return render_template('./events.html', events=events, node=node)

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

    with app.app_context():
        eventTable = EventTable(app, switchNode, interval=10)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
