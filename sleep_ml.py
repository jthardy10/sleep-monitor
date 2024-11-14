from sklearn.ensemble import RandomForestRegressor
import numpy as np
import joblib
from datetime import datetime
import os

class SleepMLAnalyzer:
    def __init__(self):
        self.model = None
        self.history = []
        self.model_path = 'models/sleep_model.joblib'
        self.is_trained = False
        os.makedirs('models', exist_ok=True)
        
        self.feature_names = [
            'heart_rate', 'temperature', 'movement', 'sound_level',
            'hour', 'day_of_week', 'time_sin', 'time_cos'
        ]
        
    def process_data(self, sensor_data, analysis_data):
        features = self._extract_features(sensor_data)
        quality = float(analysis_data['sleep_quality'])
        
        self.history.append({
            'timestamp': sensor_data['timestamp'],
            'features': features,
            'quality': quality
        })
        
        # Keep last 30 days of data
        self.history = self.history[-8640:]  # 30 days * 24 hours * 12 samples per hour
        
        # Train model if we have enough data
        if len(self.history) >= 100 and (not self.is_trained):
            self._train_model()
            
        return self._analyze_patterns(sensor_data, features)
    
    def _extract_features(self, data):
        dt = datetime.strptime(data['timestamp'], '%Y-%m-%d %H:%M:%S')
        return [
            float(data['heart_rate']),
            float(data['temperature']),
            float(data['movement']),
            float(data['sound_level']),
            dt.hour,
            dt.weekday(),
            np.sin(2 * np.pi * dt.hour / 24),
            np.cos(2 * np.pi * dt.hour / 24)
        ]
    
    def _train_model(self):
        print("Training sleep quality model...")
        X = np.array([h['features'] for h in self.history])
        y = np.array([h['quality'] for h in self.history])
        
        self.model = RandomForestRegressor(
            n_estimators=100,
            random_state=42,
            n_jobs=-1
        )
        self.model.fit(X, y)
        
        # Save model
        joblib.dump(self.model, self.model_path)
        self.is_trained = True
        print("Model training complete and saved")
    
    def _analyze_patterns(self, current_data, features):
        # Get model prediction if available
        if self.is_trained and self.model is not None:
            prediction = self.model.predict([features])[0]
        else:
            prediction = None
        
        # Analyze recent trend
        recent_qualities = [h['quality'] for h in self.history[-12:]]
        if len(recent_qualities) >= 2:
            trend = 'improving' if recent_qualities[-1] > recent_qualities[0] else 'declining'
        else:
            trend = 'stable'
        
        # Environmental analysis
        env_analysis = self._analyze_environment(current_data)
        
        return {
            'ml_prediction': prediction,
            'trend': trend,
            'environmental_analysis': env_analysis,
            'recommendations': self._generate_recommendations(current_data, env_analysis)
        }
    
    def _analyze_environment(self, data):
        return {
            'temperature': {
                'value': float(data['temperature']),
                'optimal_range': (18, 22),
                'status': 'optimal' if 18 <= float(data['temperature']) <= 22 else 'suboptimal'
            },
            'sound_level': {
                'value': float(data['sound_level']),
                'optimal_range': (0, 40),
                'status': 'optimal' if float(data['sound_level']) <= 40 else 'suboptimal'
            }
        }
    
    def _generate_recommendations(self, data, env_analysis):
        recommendations = []
        
        # Temperature recommendations
        temp = float(data['temperature'])
        if temp < 18:
            recommendations.append("Room temperature is too low. Consider increasing to 20°C")
        elif temp > 22:
            recommendations.append("Room temperature is too high. Consider decreasing to 20°C")
        
        # Sound level recommendations
        sound = float(data['sound_level'])
        if sound > 40:
            recommendations.append("High ambient noise. Consider using white noise or earplugs")
        
        # Heart rate recommendations
        hr = float(data['heart_rate'])
        if hr > 70:
            recommendations.append("Elevated heart rate. Consider relaxation techniques")
        
        # Movement recommendations
        movement = float(data['movement'])
        if movement > 0.3:
            recommendations.append("High movement detected. Consider mattress or bedding upgrade")
            
        # Feature importance based recommendations if model is trained
        if self.is_trained and self.model is not None:
            importances = self.model.feature_importances_
            sorted_features = sorted(zip(self.feature_names, importances), 
                                  key=lambda x: x[1], reverse=True)
            
            most_important = sorted_features[0]
            if most_important[1] > 0.3:  # If feature is significant
                if most_important[0] == 'temperature':
                    recommendations.append("Temperature appears to significantly impact your sleep quality")
                elif most_important[0] == 'sound_level':
                    recommendations.append("Sound levels appear to significantly impact your sleep quality")
                elif most_important[0] == 'movement':
                    recommendations.append("Movement patterns appear to significantly impact your sleep quality")
        
        return recommendations
