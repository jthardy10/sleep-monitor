# Sleep Monitor System

A secure IoT-based sleep quality monitoring system with real-time visualization.

## Features
- Real-time sleep quality monitoring
- Secure data transmission
- Interactive dashboard with Chart.js
- Sleep pattern analysis
- JWT Authentication

## Installation

```bash
# Clone the repository
git clone https://github.com/jthardy10/sleep-monitor.git
cd sleep-monitor

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configurations

# Run the application
python main.py
```

## Development

- `main` branch: Production-ready code
- `development` branch: Active development

## API Endpoints

- `/`: Dashboard interface
- `/api/token`: Authentication endpoint
- `/api/data`: Sleep monitoring data endpoint

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
