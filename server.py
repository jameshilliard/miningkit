from __future__ import division
import os
import json
import random
import time
from flask import Flask, render_template, jsonify
from pycgminer import CgminerAPI
from kit import LineChart

cgminer = CgminerAPI()

line_chart = LineChart(7)

chart_asked = time.time() - 60 * 5 # as it was asked 5 minutes ago

app = Flask(__name__)
app.debug = True

def cgsummary():
    return cgminer.summary()

def pools():
    return cgminer.pools()

def edevs():
    return cgminer.edevs()

def estats():
    return cgminer.estats()

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
            'mhs': dev['MHS 5m'],
            'ghs': dev['MHS 5m'] / 1000,
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
            'mhs': data['SUMMARY'][0]['MHS 5m'],
            'ghs': data['SUMMARY'][0]['MHS 5m'] / 1000,
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
    global chart_asked # not cool python

    now = time.time()

    if (now - chart_asked) > 60 * 5:
        line_chart.append([random.randint(200, 400), random.randint(200, 400)]);
        chart_asked = now

    return jsonify({
        'status': 'success',
        'lines': line_chart.lines()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
