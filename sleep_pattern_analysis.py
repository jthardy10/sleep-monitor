import numpy as np
from datetime import datetime, timedelta
from scipy import stats
import json

class SleepPatternAnalyzer:
    def __init__(self):
        self.sleep_history = []
        self.pattern_statistics = {}
        
    def add_data_point(self, timestamp, sensor_data, analysis):
        self.sleep_history.append({
            'timestamp': timestamp,
            'sensor_data': sensor_data,
            'analysis': analysis
        })
        self._update_statistics()
        
    def _update_statistics(self):
        if len(self.sleep_history) < 12:  # Need at least 12 data points
            return
            
        recent_data = self.sleep_history[-12:]
        
        # Sleep quality trends
        qualities = [float(d['analysis']['sleep_quality']) for d in recent_data]
        slope, _, _, _, _ = stats.linregress(range(len(qualities)), qualities)
        
        # Time-based patterns
        hour_qualities = {}
        for entry in recent_data:
            hour = datetime.strptime(entry['timestamp'], '%Y-%m-%d %H:%M:%S').hour
            if hour not in hour_qualities:
                hour_qualities[hour] = []
            hour_qualities[hour].append(float(entry['analysis']['sleep_quality']))
            
        best_hour = max(hour_qualities.items(), key=lambda x: np.mean(x[1]))[0]
        worst_hour = min(hour_qualities.items(), key=lambda x: np.mean(x[1]))[0]
        
        self.pattern_statistics = {
            'trend_slope': slope,
            'best_hour': best_hour,
            'worst_hour': worst_hour,
            'consistency': np.std(qualities),
            'improvement_rate': slope * len(qualities)
        }
        
    def get_insights(self):
        if not self.pattern_statistics:
            return "Insufficient data for pattern analysis"
            
        insights = []
        
        # Trend insights
        if self.pattern_statistics['trend_slope'] > 0.01:
            insights.append("Sleep quality is showing consistent improvement")
        elif self.pattern_statistics['trend_slope'] < -0.01:
            insights.append("Sleep quality has been declining")
            
        # Time-based insights
        insights.append(f"Best sleep quality typically occurs around {self.pattern_statistics['best_hour']}:00")
        insights.append(f"Sleep quality tends to be lower around {self.pattern_statistics['worst_hour']}:00")
        
        # Consistency insights
        if self.pattern_statistics['consistency'] < 0.1:
            insights.append("Sleep patterns are very consistent")
        elif self.pattern_statistics['consistency'] > 0.2:
            insights.append("Sleep patterns show high variability")
            
        return insights
        
    def get_optimization_suggestions(self):
        if not self.pattern_statistics:
            return []
            
        suggestions = []
        best_hour = self.pattern_statistics['best_hour']
        
        # Bedtime optimization
        ideal_bedtime = (best_hour - 1) % 24
        suggestions.append(f"Consider going to bed around {ideal_bedtime:02d}:00 for optimal sleep quality")
        
        # Consistency recommendations
        if self.pattern_statistics['consistency'] > 0.15:
            suggestions.append("Try to maintain a more consistent sleep schedule")
            
        # Improvement tracking
        if self.pattern_statistics['improvement_rate'] < 0:
            suggestions.append("Review recent changes in your sleep environment")
            
        return suggestions
        
    def get_summary_stats(self):
        if not self.pattern_statistics:
            return {}
            
        return {
            'trend': 'improving' if self.pattern_statistics['trend_slope'] > 0 else 'declining',
            'consistency_score': 1.0 - min(1.0, self.pattern_statistics['consistency'] / 0.3),
            'best_sleep_hour': self.pattern_statistics['best_hour'],
            'pattern_strength': 1.0 - min(1.0, self.pattern_statistics['consistency'] * 5)
        }

