import { Line } from 'react-chartjs-2';
import { Paper, useTheme } from '@mui/material';
import { ChartOptions } from 'chart.js';

interface SleepChartProps {
  data: {
    labels: string[];
    datasets: {
      label: string;
      data: number[];
      borderColor: string;
      backgroundColor: string;
    }[];
  };
}

export const SleepChart = ({ data }: SleepChartProps) => {
  const theme = useTheme();

  const options: ChartOptions<'line'> = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
        labels: {
          font: {
            family: theme.typography.fontFamily,
            size: 12
          },
          color: theme.palette.text.primary
        }
      },
      tooltip: {
        mode: 'index',
        intersect: false,
        backgroundColor: theme.palette.background.paper,
        titleColor: theme.palette.text.primary,
        bodyColor: theme.palette.text.secondary,
        borderColor: theme.palette.divider,
        borderWidth: 1
      }
    },
    scales: {
      x: {
        grid: {
          color: theme.palette.divider
        },
        ticks: {
          color: theme.palette.text.secondary
        }
      },
      y: {
        type: 'linear',
        beginAtZero: true,
        max: 100,
        grid: {
          color: theme.palette.divider
        },
        ticks: {
          color: theme.palette.text.secondary,
          callback: (value) => `${value}%`
        }
      }
    },
    elements: {
      line: {
        tension: 0.4
      },
      point: {
        radius: 3,
        hitRadius: 10,
        hoverRadius: 5
      }
    }
  };

  return (
    <Paper sx={{ p: 2, height: 400 }}>
      <Line data={data} options={options} />
    </Paper>
  );
};
