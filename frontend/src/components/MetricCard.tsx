import { Paper, Typography, Box } from '@mui/material';

interface MetricCardProps {
  title: string;
  value: string;
  unit: string;
  status: 'optimal' | 'warning' | 'alert';
}

export const MetricCard = ({ title, value, unit, status }: MetricCardProps) => {
  const getStatusColor = () => {
    switch (status) {
      case 'optimal':
        return '#4caf50';
      case 'warning':
        return '#ff9800';
      case 'alert':
        return '#f44336';
      default:
        return '#4caf50';
    }
  };

  return (
    <Paper 
      elevation={2}
      sx={{ 
        p: 2,
        borderRadius: 2,
        borderTop: 4,
        borderColor: getStatusColor(),
        transition: 'transform 0.3s ease-in-out',
        '&:hover': {
          transform: 'translateY(-4px)'
        }
      }}
    >
      <Typography variant="subtitle2" color="text.secondary" gutterBottom>
        {title}
      </Typography>
      <Box sx={{ display: 'flex', alignItems: 'baseline' }}>
        <Typography variant="h4" component="span" fontWeight="bold">
          {value}
        </Typography>
        <Typography variant="subtitle1" component="span" sx={{ ml: 1, color: 'text.secondary' }}>
          {unit}
        </Typography>
      </Box>
    </Paper>
  );
};
