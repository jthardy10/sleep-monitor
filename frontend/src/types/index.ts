export interface SensorData {
  heart_rate: string;
  temperature: string;
  movement: string;
  sound_level: string;
}

export interface Analysis {
  sleep_quality: string;
  status: string;
  recommendations: string[];
}

export interface SleepData {
  timestamp: string;
  sensor_data: SensorData;
  analysis: Analysis;
}
