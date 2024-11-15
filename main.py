import random
import time
import json
import threading
from datetime import datetime
from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
import logging
import eventlet

eventlet.monkey_patch()

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
socketio = SocketIO(app, 
                   cors_allowed_origins="*", 
                   logger=True, 
                   engineio_logger=True,
                   async_mode='eventlet')

connected_clients = set()

@app.route('/')
def index():
    logger.info("Index page requested")
    return render_template('dashboard.html')

@socketio.on('connect')
def handle_connect():
    client_id = request.sid
    connected_clients.add(client_id)
    logger.info(f"Client connected: {client_id} (Total clients: {len(connected_clients)})")
    emit('status', {'connected': True})

@socketio.on('disconnect')
def handle_disconnect():
    client_id = request.sid
    connected_clients.discard(client_id)
    logger.info(f"Client disconnected: {client_id} (Total clients: {len(connected_clients)})")

def generate_data():
    while True:
        try:
            now = datetime.now()
            is_sleep_time = now.hour >= 22 or now.hour <= 7
            
            if is_sleep_time:
                heart_rate = random.uniform(55, 65)
                temperature = random.uniform(20, 22)
                movement = random.uniform(0.1, 0.3)
                sound_level = random.uniform(25, 35)
            else:
                heart_rate = random.uniform(65, 85)
                temperature = random.uniform(21, 24)
                movement = random.uniform(0.2, 0.7)
                sound_level = random.uniform(35, 55)
            
            data = {
                'timestamp': now.strftime('%Y-%m-%d %H:%M:%S'),
                'sensor_data': {
                    'heart_rate': f"{heart_rate:.1f}",
                    'temperature': f"{temperature:.1f}",
                    'movement': f"{movement:.2f}",
                    'sound_level': f"{sound_level:.1f}"
                },
                'analysis': {
                    'sleep_quality': f"{random.uniform(0.4, 0.9):.2f}",
                    'status': 'optimal' if is_sleep_time else 'active',
                    'recommendations': []
                }
            }
            
            if temperature > 23:
                data['analysis']['recommendations'].append("Temperature is high")
            if sound_level > 40:
                data['analysis']['recommendations'].append("Noise level is elevated")
            if movement > 0.5:
                data['analysis']['recommendations'].append("High movement detected")
            
            if connected_clients:
                logger.info(f"Broadcasting to {len(connected_clients)} clients")
                socketio.emit('data_update', data)
            
            eventlet.sleep(5)
            
        except Exception as e:
            logger.error(f"Error generating data: {str(e)}")
            eventlet.sleep(5)

if __name__ == '__main__':
    try:
        logger.info("Starting application...")
        
        # Start data generation in background thread
        eventlet.spawn(generate_data)
        logger.info("Data generation thread started")
        
        # Start Flask application
        socketio.run(
            app,
            debug=True,
            port=8000,
            host='0.0.0.0',
            use_reloader=False
        )
    except Exception as e:
        logger.error(f"Startup error: {str(e)}")
