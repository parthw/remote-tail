import multiprocessing

from flask import Flask, json, jsonify, request

from tail_pusher import tail

app = Flask(__name__)


@app.route('/start', methods=["POST"])
def start_tailing():
    """
    Method: POST
    Input JSON: {"filepath": <value>}

    Controller to start the tailing file process
    """
    global tail_process
    content = request.get_json(silent=True)
    filepath = content["filepath"]
    try:
        if tail_process:
            if tail_process.is_alive:
                return jsonify(message=f"Currently tailing file {filepath}")
    except NameError:
        pass
    tail_process = multiprocessing.Process(target=tail, args=(filepath, ))
    tail_process.start()
    return jsonify(message=f"Started tailing file {filepath}")


@app.route('/stop')
def stop_tailing():
    """
    Method: GET

    Controller to stop the tailing file process
    """
    if tail_process.is_alive():
        tail_process.terminate()
        return jsonify(message="Stopped tailing file")
    return jsonify(message="Not tailing any file")


if __name__ == '__main__':
    app.run()
