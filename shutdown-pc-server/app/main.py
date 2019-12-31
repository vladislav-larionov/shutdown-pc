import os

from flask import Flask, request

app = Flask(__name__)
app.secret_key = 'thisMySecretKeyFOrAPP'


@app.route('/shutdown')
def shutdown() -> str:
    command = 'shutdown /s ' + '/t ' + request.args.get('time')
    os.system(command)
    return "True"


@app.route('/shutdown_cancel')
def shutdown_cancel() -> str:
    command = "shutdown /a"
    os.system(command)
    return "True"


@app.route('/connect')
def connect() -> str:
    return "True"


@app.route('/', methods=['get'])
def root() -> str:
    return "True"


@app.route('/test')
def test() -> str:
    command = request.args.get('test')
    print(command)
    return "True"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

