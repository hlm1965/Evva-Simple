# Evva-Simple

A simple Python client library for the [Evva AirKey API](https://integration.api.airkey.evva.com/docs/). This library provides an easy-to-use interface for managing locks, persons, access media, and authorizations in the Evva AirKey smart lock system.

## Features

- **Simple API**: Clean, Pythonic interface to the Evva AirKey API
- **Comprehensive**: Support for locks, persons, access media, and authorizations
- **Error Handling**: Custom exceptions for different error scenarios
- **Type Hints**: Full type annotations for better IDE support
- **Logging**: Built-in logging support for debugging

## Installation

### From source

```bash
git clone https://github.com/hlm1965/Evva-Simple.git
cd Evva-Simple
pip install -e .
```

### For development

```bash
pip install -e ".[dev]"
```

## Quick Start

```python
from evva_simple import EvvaClient

# Initialize the client with your API key
client = EvvaClient(api_key="your-api-key-here")

# List all locks
locks = client.list_locks()
print(f"Found {len(locks)} locks")

# Create a new person
person = client.create_person(
    first_name="John",
    last_name="Doe",
    email="john.doe@example.com"
)

# Create an authorization (grant access)
authorization = client.create_authorization(
    medium_id="smartphone-id",
    lock_id="lock-id",
    valid_from="2025-11-07T08:00:00Z",
    valid_to="2025-11-07T22:00:00Z"
)
```

## API Reference

### EvvaClient

The main client class for interacting with the Evva AirKey API.

#### Initialization

```python
client = EvvaClient(
    api_key="your-api-key",
    base_url=None,  # Optional: defaults to production endpoint
    timeout=30,      # Request timeout in seconds
    logger=None      # Optional: custom logger instance
)
```

#### Lock Operations

- `list_locks(offset=0, limit=100)` - List all locks
- `get_lock(lock_id)` - Get details of a specific lock

#### Person Operations

- `list_persons(offset=0, limit=100)` - List all persons
- `get_person(person_id)` - Get details of a specific person
- `create_person(first_name, last_name, email=None, phone=None)` - Create a new person
- `delete_person(person_id)` - Delete a person

#### Authorization Operations

- `list_authorizations(offset=0, limit=100)` - List all authorizations
- `create_authorization(medium_id, lock_id, valid_from, valid_to)` - Grant access
- `delete_authorization(authorization_id)` - Revoke access

#### Access Media Operations

- `list_media(offset=0, limit=100)` - List all access media (smartphones, cards, etc.)
- `get_medium(medium_id)` - Get details of a specific access medium

## Examples

See [`example.py`](example.py) for a complete working example.

### List all locks

```python
locks = client.list_locks()
for lock in locks:
    print(f"{lock['name']}: {lock['id']}")
```

### Grant temporary access

```python
from datetime import datetime, timedelta

# Grant access for today
now = datetime.utcnow()
valid_from = now.isoformat() + "Z"
valid_to = (now + timedelta(hours=8)).isoformat() + "Z"

authorization = client.create_authorization(
    medium_id="smartphone-id",
    lock_id="lock-id",
    valid_from=valid_from,
    valid_to=valid_to
)
```

## Error Handling

The library provides custom exceptions for different error scenarios:

```python
from evva_simple import (
    EvvaAPIError,           # Base exception
    EvvaAuthenticationError,  # Invalid API key
    EvvaNotFoundError,       # Resource not found
    EvvaValidationError      # Invalid request data
)

try:
    lock = client.get_lock("invalid-id")
except EvvaNotFoundError:
    print("Lock not found")
except EvvaAuthenticationError:
    print("Invalid API key")
except EvvaAPIError as e:
    print(f"API error: {e}")
```

## Getting Your API Key

1. Register your AirKey system at https://airkey.evva.com
2. Go to Settings > AirKey Cloud Interface (API)
3. Activate the API and obtain your API key
4. **Important**: Save the API key securely - it's only shown once!

## Requirements

- Python 3.8 or higher
- `requests` library

## Development

### Running tests

```bash
pytest
```

### Code formatting

```bash
black evva_simple/
```

### Type checking

```bash
mypy evva_simple/
```

## License

MIT License - see LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Disclaimer

This is an unofficial client library and is not affiliated with or endorsed by EVVA Sicherheitstechnologie GmbH. Use at your own risk.

## Resources

- [Evva AirKey Official Website](https://www.evva.com/int-en/products/electronic-locking-systems-accesscontrol-systems/airkey/)
- [Evva AirKey API Documentation](https://integration.api.airkey.evva.com/docs/)
- [Evva Support](https://www.evva.com/int-en/service-support/)