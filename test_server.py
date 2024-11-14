import time
from flask import Flask, jsonify
from flask_socketio import SocketIO, emit
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/test')
def test():
    return jsonify({"status": "ok"})

@socketio.on('connect')
def handle_connect():
    logger.info("Client connected")
    emit('status', {'data': 'Connected'})

@socketio.on('disconnect')
def handle_disconnect():
    logger.info("Client disconnected")

def run_server():
    try:
        logger.info("Starting test server...")
        socketio.run(app, port=8001, debug=True)
    except Exception as e:
        logger.error(f"Server error: {e}")

if __name__ == "__main__":
    run_server()
