import { create } from 'zustand';

interface SleepData {
  timestamp: string;
  sensor_data: {
    heart_rate: string;
    temperature: string;
    movement: string;
    sound_level: string;
  };
  analysis: {
    sleep_quality: string;
    status: string;
    recommendations: string[];
  };
}

interface SleepStore {
  currentData: SleepData | null;
  historicalData: SleepData[];
  setCurrentData: (data: SleepData) => void;
  addHistoricalData: (data: SleepData) => void;
}

export const useSleepStore = create<SleepStore>((set) => ({
  currentData: null,
  historicalData: [],
  setCurrentData: (data) => set({ currentData: data }),
  addHistoricalData: (data) =>
    set((state) => ({
      historicalData: [...state.historicalData.slice(-30), data],
    })),
}));
