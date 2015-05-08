from __future__ import division
import os
import json
import random
from flask import Flask, render_template, jsonify

app = Flask(__name__)
app.debug = True

def random_line(size):
    return [random.randrange(1, 100) for x in xrange(1, size + 1)]

def random_lines(line_size):
    lines = []

    for i in xrange(1, random.randint(2, 4)):
        lines.append(random_line(line_size))

    return lines

def cgsummary():
    with open('json/summary.json') as f:
        return json.load(f)

def pools():
    with open('json/pools.json') as f:
        return json.load(f)

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

@app.route('/summary.json')
def summary():
    data = cgsummary()
    pools_data = pools()

    total = data['SUMMARY'][0]['Accepted'] + data['SUMMARY'][0]['Rejected']
    accepted_percent = int(data['SUMMARY'][0]['Accepted'] / total * 100)
    rejected_percent = int(data['SUMMARY'][0]['Rejected'] / total * 100)

    response = {
        'status': 'success',
        'summary': {
            'mhs': data['SUMMARY'][0]['MHS 5s'],
            'ghs': data['SUMMARY'][0]['MHS 5s'] / 1000,
            'accepted': data['SUMMARY'][0]['Accepted'],
            'rejected': data['SUMMARY'][0]['Rejected'],
            'accepted_percent': accepted_percent,
            'rejected_percent': rejected_percent,
            'pool': {
                'url': pools_data['POOLS'][0]['URL'],
                'user': pools_data['POOLS'][0]['User']
            }
        }
    }

    return jsonify(response)

@app.route('/chart.json')
def chart():
    return jsonify({
        'status': 'success',
        'lines': random_lines(7)
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
