# Testing Guide

## Running Tests

### Unit Tests
```bash
pytest tests/
```

### Integration Tests
```bash
python run_tests.py
```

### Client Tests
```bash
python test_client.py
```

## Test Structure

### Unit Tests
- API endpoints
- Data processing
- Analysis functions

### Integration Tests
- WebSocket connections
- Data flow
- ML components

### Performance Tests
- Connection handling
- Data processing
- Analysis timing

## Coverage
```bash
pytest --cov=. tests/
```

## Writing Tests

### Categories
1. Unit Tests (tests/)
2. Integration Tests (test_*.py)
3. Client Tests (test_client.py)
4. Server Tests (test_server.py)

### Best Practices
- Test isolation
- Mock external services
- Clear assertions
- Full coverage
