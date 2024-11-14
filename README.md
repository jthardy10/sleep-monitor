# Sleep Monitor System

Real-time sleep monitoring system with ML-based analysis and pattern detection.

## Features
- Real-time sleep quality monitoring 
- Machine learning-based pattern analysis
- Interactive dashboard with live graphs
- Environmental factor analysis
- Smart recommendations
- Secure data transmission

## Quick Start
```bash
# Clone the repository
git clone https://github.com/jthardy10/sleep-monitor.git

# Install dependencies
pip install -r requirements.txt

# Start the application
python main.py
```

Access the dashboard at `http://localhost:8000`

## System Structure
```
sleep-monitor/
├── main.py              # Main application server
├── sleep_ml.py         # Machine learning components
├── secure_transmission.py  # Secure data handling
├── templates/          # Frontend templates
└── tests/             # Test suite
```

## Technology Stack
- Flask (Backend server)
- Socket.IO (Real-time communication)
- Chart.js (Data visualisation)
- scikit-learn (Machine learning)
- AWS DynamoDB (Data storage)

## Documentation
- [Setup Guide](docs/setup/README.md)
- [API Documentation](docs/api/README.md)
- [Features Guide](docs/features/README.md)
- [Testing Guide](docs/testing/README.md)

## Contributing
Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on our code of conduct and the process for submitting pull requests.

## Licence
This project is licensed under the MIT Licence - see the [LICENCE](LICENCE) file for details.
