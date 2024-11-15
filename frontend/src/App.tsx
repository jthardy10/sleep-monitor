import { useEffect, useState } from 'react';
import { Container, Grid, Box, Typography, Paper } from '@mui/material';
import { io } from 'socket.io-client';
import { MetricCard } from './components/MetricCard';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler,
  ChartOptions
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

const socket = io('http://localhost:8000', {
  transports: ['websocket'],
  reconnection: true,
  reconnectionAttempts: Infinity,
  reconnectionDelay: 1000,
  reconnectionDelayMax: 5000,
  timeout: 20000,
});

function App() {
  const [data, setData] = useState<any>(null);
  const [history, setHistory] = useState<any[]>([]);

  useEffect(() => {
    socket.on('connect', () => {
      console.log('Connected to server');
    });

    socket.on('data_update', (newData) => {
      console.log('Received data:', newData);
      setData(newData);
      setHistory(prev => {
        const newHistory = [...prev, newData];
        return newHistory.slice(-30); // Keep last 30 data points
      });
    });

    return () => {
      socket.off('connect');
      socket.off('data_update');
    };
  }, []);

  const getMetricStatus = (value: number, thresholds: { warning: number; alert: number }) => {
    if (value >= thresholds.alert) return 'alert';
    if (value >= thresholds.warning) return 'warning';
    return 'optimal';
  };

  const chartData = {
    labels: history.map(d => new Date(d.timestamp).toLocaleTimeString()),
    datasets: [
      {
        label: 'Sleep Quality',
        data: history.map(d => parseFloat(d.analysis.sleep_quality) * 100),
        borderColor: 'rgb(75, 192, 192)',
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        fill: true,
        tension: 0.4
      }
    ]
  };

  const chartOptions: ChartOptions<'line'> = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top' as const,
      },
      tooltip: {
        mode: 'index',
        intersect: false,
        callbacks: {
          label: function(context) {
            return `${context.parsed.y.toFixed(1)}%`;
          }
        }
      }
    },
    scales: {
      y: {
        type: 'linear' as const,
        beginAtZero: true,
        max: 100,
        ticks: {
          callback: function(value) {
            return `${value}%`;
          }
        }
      }
    }
  };

  return (
    <Box sx={{ bgcolor: '#f5f5f5', minHeight: '100vh', py: 4 }}>
      <Container>
        <Typography variant="h4" gutterBottom sx={{ fontWeight: 'bold', color: '#1a237e' }}>
          Sleep Monitor
        </Typography>
        <Grid container spacing={3}>
          {data && (
            <>
              <Grid item xs={12} sm={6} md={3}>
                <MetricCard
                  title="Heart Rate"
                  value={data.sensor_data.heart_rate}
                  unit="BPM"
                  status={getMetricStatus(parseFloat(data.sensor_data.heart_rate), { warning: 75, alert: 85 })}
                />
              </Grid>
              <Grid item xs={12} sm={6} md={3}>
                <MetricCard
                  title="Temperature"
                  value={data.sensor_data.temperature}
                  unit="°C"
                  status={getMetricStatus(parseFloat(data.sensor_data.temperature), { warning: 23, alert: 24 })}
                />
              </Grid>
              <Grid item xs={12} sm={6} md={3}>
                <MetricCard
                  title="Movement"
                  value={data.sensor_data.movement}
                  unit="units"
                  status={getMetricStatus(parseFloat(data.sensor_data.movement), { warning: 0.4, alert: 0.6 })}
                />
              </Grid>
              <Grid item xs={12} sm={6} md={3}>
                <MetricCard
                  title="Sound Level"
                  value={data.sensor_data.sound_level}
                  unit="dB"
                  status={getMetricStatus(parseFloat(data.sensor_data.sound_level), { warning: 40, alert: 50 })}
                />
              </Grid>
            </>
          )}
          
          <Grid item xs={12}>
            <Paper sx={{ p: 2, mb: 3, height: '400px' }}>
              <Typography variant="h6" gutterBottom>
                Sleep Quality Trend
              </Typography>
              <Line data={chartData} options={chartOptions} />
            </Paper>
          </Grid>

          <Grid item xs={12}>
            <Paper sx={{ p: 2 }}>
              <Typography variant="h6" gutterBottom>
                Raw Data
              </Typography>
              <pre style={{ margin: 0, overflow: 'auto' }}>
                {data ? JSON.stringify(data, null, 2) : 'Waiting for data...'}
              </pre>
            </Paper>
          </Grid>
        </Grid>
      </Container>
    </Box>
  );
}

export default App;
