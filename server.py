import os
from flask import Flask, render_template

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
