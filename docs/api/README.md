# API Documentation

## WebSocket Events

### Connection
- `connect`: Client connection
- `disconnect`: Client disconnection
- `error`: Connection error

### Data Events
```javascript
// Data Update Event
{
    "sensor_data": {
        "heart_rate": "65.0",
        "temperature": "21.5",
        "movement": "0.1",
        "sound_level": "35.0"
    },
    "analysis": {
        "sleep_quality": "0.85",
        "recommendations": []
    },
    "timestamp": "2024-11-14T12:00:00"
}
```

## REST Endpoints

### GET /
Returns dashboard interface

### POST /api/token
Returns authentication token
```javascript
{
    "token": "eyJhbGciOiJ..."
}
```

## Security
- SSL/TLS encryption
- JWT authentication
- Encrypted payloads
