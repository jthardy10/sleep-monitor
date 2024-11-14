# Setup Guide

## Prerequisites
- Python 3.8+
- pip
- Virtual environment (recommended)

## Installation Steps

1. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Environment Setup:
- Copy `.env.example` to `.env`
- Update with your configuration values

4. SSL Certificates:
```bash
openssl req -x509 -newkey rsa:4096 -nodes -out server.crt -keyout server.key -days 365
```

5. Start Application:
```bash
python main.py
```

## Configuration
- Port: 8000 (default)
- Debug: False (production)
- SSL: Enabled
- Database: DynamoDB

## AWS Configuration
1. Create DynamoDB table
2. Set AWS credentials in `.env`
3. Run connection test:
```bash
python test_aws.py
```
