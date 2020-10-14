"""
Deamon to be set up on the server to check sums.
"""

import argparse
from flask import Flask, jsonify, request
import socket
from pathlib import Path
from platform import system as OS

from fs_ops.checksums import check_sum


ap = argparse.ArgumentParser(description='Run a deamon that checks sums of sent files.',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
ARG = ap.add_argument

ARG('--host', help="Host's IP.", default=socket.gethostbyname(socket.gethostname()))
ARG('--port', help='Port to listen to.', default=9002, type=int)
ARG('--debug', action='store_true', help='Run in debug mode.')
ap = ap.parse_args()
app = Flask(__name__)


@app.route('/')
def index():
    return f'msyncd operating.\nIP: {ap.host} PORT: {ap.port}'


@app.route('/check', methods=['POST'])
def get_project_id():
    if request.data:
        if ap.debug:
            print(request.data)
        server_path = request.get_json()
        cs = check_sum(server_path)
        if ap.debug:
            print(cs)
        return jsonify(cs)


if __name__ == '__main__':
    app.run(debug=ap.debug,
            host=ap.host,
            port=ap.port,
            threaded=True)