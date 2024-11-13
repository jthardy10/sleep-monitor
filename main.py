import random
import time
import json
import threading
import jwt
from datetime import datetime, timedelta
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import numpy as np
from collections import deque
from decimal import Decimal

# Add secret key for JWT
SECRET_KEY = 'your-secret-key-here'

class DataStore:
    def __init__(self, max_size=1000):
        self.sensor_data = deque(maxlen=max_size)
        self.analysis_data = deque(maxlen=max_size)
        
    def add_reading(self, sensor_data, analysis):
        self.sensor_data.append(sensor_data)
        self.analysis_data.append(analysis)
    
    def get_recent_data(self, n=100):
        return list(self.sensor_data)[-n:], list(self.analysis_data)[-n:]

class SimulatedSensors:
    def __init__(self):
        self.base_heart_rate = Decimal('65.0')
        self.base_temperature = Decimal('21.5')
        self.base_movement = Decimal('0.1')
        self.time_of_day = 0
        
    def get_readings(self):
        self.time_of_day = (self.time_of_day + 1) % 24
        is_sleep_time = 22 <= self.time_of_day or self.time_of_day <= 7
        
        if is_sleep_time:
            heart_rate = self.base_heart_rate + Decimal(str(random.uniform(-10, 5)))
            temperature = self.base_temperature + Decimal(str(random.uniform(-0.5, 0.5)))
            movement = max(Decimal('0'), self.base_movement + Decimal(str(random.uniform(-0.05, 0.15))))
            sound_level = Decimal(str(random.uniform(20, 40)))
        else:
            heart_rate = self.base_heart_rate + Decimal(str(random.uniform(0, 30)))
            temperature = self.base_temperature + Decimal(str(random.uniform(-1, 1)))
            movement = self.base_movement + Decimal(str(random.uniform(0, 0.5)))
            sound_level = Decimal(str(random.uniform(30, 70)))
            
        return {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'heart_rate': str(round(heart_rate, 1)),
            'temperature': str(round(temperature, 2)),
            'movement': str(round(movement, 3)),
            'sound_level': str(round(sound_level, 1))
        }

class SleepAnalyzer:
    def __init__(self):
        self.ideal_ranges = {
            'heart_rate': (50, 70),
            'temperature': (18, 22),
            'movement': 0.2,
            'sound_level': 40
        }
        
    def analyze_sleep_quality(self, data):
        heart_score = self._score_vital(float(data['heart_rate']), 
            self.ideal_ranges['heart_rate'][0],
            self.ideal_ranges['heart_rate'][1])
        temp_score = self._score_vital(float(data['temperature']),
            self.ideal_ranges['temperature'][0],
            self.ideal_ranges['temperature'][1])
        movement_score = max(0, 1 - float(data['movement'])/self.ideal_ranges['movement'])
        sound_score = max(0, 1 - float(data['sound_level'])/self.ideal_ranges['sound_level'])
        
        quality = (heart_score + temp_score + movement_score + sound_score) / 4
        
        return {
            'timestamp': data['timestamp'],
            'sleep_quality': str(round(quality, 2)),
            'scores': {
                'heart_rate': str(round(heart_score, 2)),
                'temperature': str(round(temp_score, 2)),
                'movement': str(round(movement_score, 2)),
                'sound': str(round(sound_score, 2))
            }
        }
    
    def _score_vital(self, value, min_val, max_val):
        if min_val <= value <= max_val:
            return 1.0
        elif value < min_val:
            return max(0, 1 - (min_val - value)/(min_val/2))
        else:
            return max(0, 1 - (value - max_val)/(max_val/2))

app = Flask(__name__)
CORS(app)
data_store = DataStore()

def require_token(f):
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'error': 'No token provided'}), 401
        try:
            jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            return f(*args, **kwargs)
        except:
            return jsonify({'error': 'Invalid token'}), 401
    return decorated

@app.route('/api/token', methods=['POST'])
def get_token():
    token = jwt.encode(
        {
            'exp': datetime.utcnow() + timedelta(hours=24)
        },
        SECRET_KEY,
        algorithm='HS256'
    )
    return jsonify({'token': token})

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/api/data')
@require_token
def get_data():
    sensor_data, analysis_data = data_store.get_recent_data(100)
    return jsonify({
        'sensor_data': sensor_data,
        'analysis_data': analysis_data
    })

def simulation_thread():
    sensors = SimulatedSensors()
    analyzer = SleepAnalyzer()
    
    while True:
        sensor_data = sensors.get_readings()
        analysis = analyzer.analyze_sleep_quality(sensor_data)
        data_store.add_reading(sensor_data, analysis)
        time.sleep(5)

if __name__ == '__main__':
    sim_thread = threading.Thread(target=simulation_thread, daemon=True)
    sim_thread.start()
    print("Starting Secure Sleep Monitor Simulation...")
    print("Open http://localhost:5000 in your web browser")
    app.run(debug=False)
