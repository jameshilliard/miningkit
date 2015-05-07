import os
import json
from flask import Flask, render_template, jsonify

app = Flask(__name__)
app.debug = True

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
    with open('json/edevs.json') as f:
        data = json.load(f)

    response = {
        'status': 'success',
        'devices': []
    }

    for dev in data['DEVS']:
        response['devices'].append({
            'id': dev['ID'],
            'name': dev['Name'],
            'mhs': dev['MHS 5s'],
            'ghs': dev['MHS 5s'] / 1000,
            'temperature': dev['Temperature'],
            'accepted': dev['Accepted'],
            'rejected': dev['Rejected']
        })

    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
