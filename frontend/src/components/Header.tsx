import { AppBar, Toolbar, Typography } from '@mui/material';

export const Header = () => (
  <AppBar position="static" sx={{ mb: 3 }}>
    <Toolbar>
      <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
        Sleep Monitor Dashboard
      </Typography>
    </Toolbar>
  </AppBar>
);
