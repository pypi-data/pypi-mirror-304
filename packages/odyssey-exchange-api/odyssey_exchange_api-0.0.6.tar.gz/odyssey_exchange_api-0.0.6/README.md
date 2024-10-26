# Odyssey Exchange API Library

A Python library for interacting with *[odyssey.trade](https://odyssey.trade)* API, allowing developers to easily
integrate trading functionalities into their applications.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)
- [License](#license)

## Features

- Full support of Odyssey Exchange Spot API at 01.10.2024.
- Full support of Odyssey Exchange Futures API at 01.10.2024.
- Full support of Odyssey Exchange WebSocket API at 01.10.2024.
- Synchronous and asynchronous support.
- All objects are typed and documented.

## Installation

You can install the library via pip:

```bash
pip install odyssey_exchange_api
```

## Usage

To get started with the library, import it in your Python script:

```python
import odyssey_exchange_api
```

### Example Initialization

#### Sync API

```python
from odyssey_exchange_api import SyncOdysseyExchangeAPI

api = SyncOdysseyExchangeAPI(api_key='YOUR_API_KEY', secret_key='YOUR_API_SECRET')
```

#### Async API

```python
from odyssey_exchange_api import AsyncOdysseyExchangeAPI

api = AsyncOdysseyExchangeAPI(api_key='YOUR_API_KEY', secret_key='YOUR_API_SECRET')
```

## Examples

### Ping

```python
request = SpotPingRequest()
response = api.make_request(request)
print(response)
```

### Fetching Recent Trades

```python
request = SpotRecentTradesRequest(symbol='BTCUSDT')
response = api.make_request(request)
print(response)
```

### Placing a New Order

```python
request = SpotCreateOrderRequest(
    symbol="BCUSDT",
    volume=Decimal("0.01"),
    side=SpotOrderSide.BUY,
    type=SpotOrderType.LIMIT,
    price=Decimal("56000")
)
response = api.make_request(request)
print(response)
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.