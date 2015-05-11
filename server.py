from __future__ import division
import os
import time
from flask import Flask, render_template, jsonify
from kit import LineChart, Cgminer, CgminerError

line_chart = LineChart(7)

chart_asked = time.time() - 60 * 5 # as it was asked 5 minutes ago

app = Flask(__name__)
app.debug = True

@app.route('/')
def status():
    return render_template('status.html')

@app.route('/miner')
def miner():
    return render_template('miner.html')

@app.route('/update_pools', methods=['POST'])
def update_pools():
    cgminer = Cgminer()
    cgminer.save(os.path.dirname(os.path.realpath(__file__)) + '/config/cgminer')

    return 'Hello world!'

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
            'message': 'CgminerError: ' + e.message,
            'devices': []
        }
    except Exception as e:
        response = {
            'status': 'error',
            'message': 'Exception: ' + e.message,
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
            'message': 'CgminerError: ' + e.message,
            'summary': {}
        }
    except Exception as e:
        response = {
            'status': 'error',
            'message': 'Exception: ' + e.message,
            'devices': []
        }

    return jsonify(response)

@app.route('/chart.json')
def chart():
    global chart_asked # not cool python
    cgminer = Cgminer()

    now = time.time()

    if (now - chart_asked) > 60 * 5:
        try:
            line_chart.append(cgminer.latest_hashrate_poins())
            chart_asked = now
        except CgminerError as e:
            return jsonify({
                'status': 'error',
                'message': 'CgminerError: ' + e.message,
                'lines': []
            })
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': 'Exception: ' + e.message,
                'lines': []
            })

    return jsonify({
        'status': 'success',
        'lines': line_chart.lines()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
