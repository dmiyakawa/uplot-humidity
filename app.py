from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import time
import random
import math
import os

app = Flask(__name__)
CORS(app)

start_time = time.time()

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/api/data')
def get_data():
    current_time = time.time()
    elapsed = current_time - start_time
    
    # Generate sine wave with noise for humidity-like data
    base_value = 50 + 20 * math.sin(elapsed / 60)  # 60 second cycle
    noise = random.uniform(-5, 5)
    humidity = max(0, min(100, base_value + noise))
    
    # Generate temperature data
    temp_base = 22 + 8 * math.sin(elapsed / 120)  # 120 second cycle
    temp_noise = random.uniform(-2, 2)
    temperature = temp_base + temp_noise
    
    return jsonify({
        'timestamp': int(current_time * 1000),  # milliseconds
        'humidity': round(humidity, 1),
        'temperature': round(temperature, 1)
    })

@app.route('/api/history')
def get_history():
    current_time = time.time()
    data = []
    
    # Generate last 60 seconds of data
    for i in range(60):
        timestamp = current_time - (59 - i)
        elapsed = timestamp - start_time
        
        base_value = 50 + 20 * math.sin(elapsed / 60)
        noise = random.uniform(-5, 5)
        humidity = max(0, min(100, base_value + noise))
        
        temp_base = 22 + 8 * math.sin(elapsed / 120)
        temp_noise = random.uniform(-2, 2)
        temperature = temp_base + temp_noise
        
        data.append({
            'timestamp': int(timestamp * 1000),
            'humidity': round(humidity, 1),
            'temperature': round(temperature, 1)
        })
    
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)