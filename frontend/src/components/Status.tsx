import { Alert, Fade } from '@mui/material';
import WifiIcon from '@mui/icons-material/Wifi';
import WifiOffIcon from '@mui/icons-material/WifiOff';

interface StatusProps {
  isConnected: boolean;
}

export const Status = ({ isConnected }: StatusProps) => (
  <Fade in={!isConnected}>
    <Alert 
      icon={isConnected ? <WifiIcon /> : <WifiOffIcon />}
      severity={isConnected ? "success" : "warning"}
      sx={{ 
        mb: 2,
        '& .MuiAlert-icon': {
          animation: isConnected ? 'none' : 'pulse 1.5s infinite'
        }
      }}
    >
      {isConnected ? 'Connected to server' : 'Connecting to server...'}
    </Alert>
  </Fade>
);
