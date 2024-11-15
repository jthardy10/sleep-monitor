import { useContext } from 'react';
import { ThemeContext } from '../context/ThemeContext';

export const useColorMode = () => {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useColorMode must be used within a ThemeProvider');
  }
  return context;
};
