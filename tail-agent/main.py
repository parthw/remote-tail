"""
Tail Agent
Main file with controllers
"""
import multiprocessing

from flask import Flask, jsonify, request

from tailer import tail

app = Flask(__name__)


@app.route('/start', methods=["POST"])
def start_tailing():
    """
    Method: POST
    Input JSON: {"filepath": <value>}

    Controller to start the tailing file process
    """
    global TAIL_PROCESS
    content = request.get_json(silent=True)
    filepath = content["filepath"]
    try:
        if TAIL_PROCESS:
            if TAIL_PROCESS.is_alive:
                return jsonify(message=f"Currently tailing file {filepath}")
    except NameError:
        pass
    TAIL_PROCESS = multiprocessing.Process(target=tail, args=(filepath, ))
    TAIL_PROCESS.start()
    return jsonify(message=f"Started tailing file {filepath}")


@app.route('/stop')
def stop_tailing():
    """
    Method: GET

    Controller to stop the tailing file process
    """
    if TAIL_PROCESS.is_alive():
        TAIL_PROCESS.terminate()
        return jsonify(message="Stopped tailing file")
    return jsonify(message="Not tailing any file")


@app.route('/status')
def application_status():
    """
    Method: GET

    Controller to get the status of application 
    """
    return jsonify(message="running")


if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=5000,
        threaded=True
    )
