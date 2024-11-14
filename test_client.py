import socketio
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_connection():
    sio = socketio.Client()
    
    @sio.event
    def connect():
        logger.info("Connected!")
    
    @sio.event
    def disconnect():
        logger.info("Disconnected!")
    
    @sio.on('status')
    def on_status(data):
        logger.info(f"Received status: {data}")
    
    try:
        sio.connect('http://localhost:8000')
        logger.info("Waiting for messages...")
        time.sleep(5)
        sio.disconnect()
    except Exception as e:
        logger.error(f"Test failed: {e}")

if __name__ == "__main__":
    test_connection()
