import os
import json
from flask import Flask, render_template, jsonify

app = Flask(__name__)
app.debug = True

def edevs():
    with open('json/edevs.json') as f:
        return json.load(f)

def estats():
    with open('json/estats.json') as f:
        return json.load(f)

@app.route('/')
def status():
    return render_template('status.html')

@app.route('/miner')
def miner():
    return render_template('miner.html')

@app.route('/panel')
def panel():
    return render_template('panel.html')

@app.route('/alerts')
def alerts():
    return render_template('alerts.html')

@app.route('/log')
def log():
    with os.popen('tail /var/log/boot.log -n 30') as f:
        log = f.read()

    return render_template('log.html', log=log)

# json
@app.route('/devices.json')
def devices():
    data = {
        'edevs': edevs(),
        'estats': estats()
    }

    response = {
        'status': 'success',
        'devices': []
    }

    for i in xrange(0, len(data['edevs']['DEVS'])):
        dev = data['edevs']['DEVS'][i]
        stat = data['estats']['STATS'][i]

        response['devices'].append({
            'id': dev['ID'],
            'name': dev['Name'],
            'mhs': dev['MHS 5s'],
            'ghs': dev['MHS 5s'] / 1000,
            'temperature': dev['Temperature'],
            'accepted': dev['Accepted'],
            'rejected': dev['Rejected'],
            'clockrate': stat['base clockrate'],
            'fan': stat['fan percent'],
            'voltage': stat['Asic0 voltage 0']
        })

    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
