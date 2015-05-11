from __future__ import division
import os
import json
import random
import time
from flask import Flask, render_template, jsonify
from pycgminer import CgminerAPI
from kit import LineChart, Cgminer, CgminerError

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
    cgminer = Cgminer()

    try:
        response = {
            'status': 'success',
            'devices': cgminer.devices()
        }
    except CgminerError as e:
        response = {
            'status': 'error',
            'message': e.message,
            'devices': []
        }

    return jsonify(response)

@app.route('/summary.json')
def summary():
    cgminer = Cgminer()

    try:
        response = {
            'status': 'success',
            'summary': cgminer.summary()
        }
    except CgminerError as e:
        response = {
            'status': 'error',
            'message': e.message,
            'summary': {}
        }

    return jsonify(response)

@app.route('/chart.json')
def chart():
    global chart_asked # not cool python

    now = time.time()

    if (now - chart_asked) > 60 * 5:
        points = []
        for edev in edevs()['DEVS']:
            points.append(edev['MHS 5m'] / 1000)

        line_chart.append(points)
        chart_asked = now

    return jsonify({
        'status': 'success',
        'lines': line_chart.lines()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
