import { Paper, Typography, List, ListItem, ListItemIcon, ListItemText } from '@mui/material';
import WarningIcon from '@mui/icons-material/Warning';

interface RecommendationsProps {
  recommendations: string[];
}

export const Recommendations = ({ recommendations }: RecommendationsProps) => {
  if (!recommendations.length) return null;

  return (
    <Paper sx={{ p: 2 }}>
      <Typography variant="h6" gutterBottom>
        Recommendations
      </Typography>
      <List>
        {recommendations.map((recommendation, index) => (
          <ListItem key={index}>
            <ListItemIcon>
              <WarningIcon color="warning" />
            </ListItemIcon>
            <ListItemText primary={recommendation} />
          </ListItem>
        ))}
      </List>
    </Paper>
  );
};
