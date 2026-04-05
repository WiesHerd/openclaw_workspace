# Bitcoin Price Tracker Code Review

## Overview
The Bitcoin price tracker script is well-structured and demonstrates good Python practices. It fetches Bitcoin price data from CoinGecko API and calculates a 7-day simple moving average. Below are specific observations and improvement suggestions across the requested categories.

## Error Handling
### Strengths:
- Specific exception handling for HTTP errors (including 429 rate limit), connection errors, and timeouts
- Appropriate logging of errors with context
- Clean exit with proper exit codes in main()
- ValueError handling for data validation issues

### Improvements:
1. **Add retry logic for transient failures**: Implement exponential backoff for connection errors and timeouts
2. **Handle partial data failures**: Consider what to do if some price entries are malformed rather than skipping them silently
3. **Add circuit breaker pattern**: For production use, consider implementing a circuit breaker to prevent cascading failures
4. **More specific error types**: Create custom exception types for different failure modes (APIError, DataError, etc.)

## API Rate Limiting
### Strengths:
- Explicit handling of HTTP 429 status code with clear user message
- Timeout set on requests (15 seconds) prevents hanging

### Improvements:
1. **Implement retry-after respect**: Check for Retry-After header in 429 responses and wait accordingly
2. **Add exponential backoff**: For rate limit errors, implement jittered exponential backoff
3. **Track rate limit headers**: Log X-Ratelimit-Limit and X-Ratelimit-Remaining headers if provided by API
4. **Configurable request throttling**: Add option to delay between requests to stay well within limits
5. **Consider API key usage**: If available, use CoinGecko Pro API for higher rate limits

## Code Structure
### Strengths:
- Clear separation of concerns (data fetching, calculation, display)
- Good function decomposition with single responsibilities
- Effective use of constants (COINGECKO_API_URL)
- Proper use of `__name__ == "__main__"` guard
- Meaningful function and variable names

### Improvements:
1. **Extract API client**: Create a CoinGeckoClient class to encapsulate API interactions
2. **Configuration management**: Move constants to a config module or use environment variables
3. **Dependency injection**: Allow injecting requests session for easier testing
4. **Separate CLI from logic**: Make core functions importable without running the display logic
5. **Add data validation layer**: Consider using pydantic or similar for data validation

## Type Safety
### Strengths:
- Consistent use of type hints throughout
- Proper use of `from __future__ import annotations`
- Appropriate use of Optional types where values can be None
- Good use of TypedDict equivalent with dict[str, Any]

### Improvements:
1. **Replace Any with specific types**: Define TypedDict for price data structure
2. **Use Protocol for interfaces**: Define protocols for API client to improve testability
3. **More precise numeric types**: Consider using NewType or custom classes for domain-specific values (price, timestamp)
4. **Add type comments for complex logic**: Especially in the SMA calculation
5. **Enable strict type checking**: Configure mypy or similar in development workflow

## Production Readiness
### Strengths:
- Proper logging configuration with appropriate format and level
- Clean error handling and exit strategies
- Timeout on external requests prevents resource exhaustion
- Handles edge cases (empty data, insufficient data for SMA)
- No hard-coded credentials or secrets

### Improvements:
1. **Add command-line interface**: Use argparse to make days, window, and other parameters configurable
2. **Environment configuration**: Allow API URL, timeout, and other settings via environment variables
3. **Add health check endpoint**: If extended to a service, add /health or similar
4. **Implement caching**: Cache API responses to reduce redundant requests and improve performance
5. **Add metrics collection**: Track request counts, latency, error rates for monitoring
6. **Add unit tests**: Create test suite covering normal operation, error cases, and edge cases
7. **Add integration tests**: Test against actual API (with mocking or testnet)
8. **Consider async version**: For high-frequency updates, consider async implementation
9. **Add packaging**: Convert to proper Python package with setup.py/pyproject.toml
10. **Add Docker support**: Containerize for easy deployment

## Specific Implementation Suggestions

### 1. Enhanced Rate Limiting
```python
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def create_session_with_retries():
    session = requests.Session()
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session
```

### 2. Improved Type Safety
```python
from typing import TypedDict

class PriceData(TypedDict):
    date: datetime.date
    price_usd: float
    sma_7d: float | None

def fetch_btc_price_history(days: int = 30) -> list[PriceData]:
    # implementation
```

### 3. Configurable Parameters
```python
import os
from dataclasses import dataclass

@dataclass
class Config:
    api_url: str = os.getenv("COINGECKO_API_URL", "https://api.coingecko.com/api/v3")
    timeout: int = int(os.getenv("REQUEST_TIMEOUT", "15"))
    default_days: int = int(os.getenv("DEFAULT_DAYS", "30"))
    sma_window: int = int(os.getenv("SMA_WINDOW", "7"))

def main(config: Config | None = None) -> None:
    config = config or Config()
    # rest of implementation
```

### 4. CLI Enhancement
```python
import argparse

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Track Bitcoin price and calculate SMA")
    parser.add_argument(
        "--days", 
        type=int, 
        default=30, 
        help="Number of days of historical data to fetch"
    )
    parser.add_argument(
        "--window", 
        type=int, 
        default=7, 
        help="SMA window size in days"
    )
    parser.add_argument(
        "--verbose", 
        action="store_true", 
        help="Enable verbose logging"
    )
    return parser.parse_args()
```

## Summary
The script demonstrates solid foundational Python practices with clear structure, good error handling, and appropriate use of type hints. For production use, the main areas for enhancement are:

1. **Resilience**: Add retry mechanisms with exponential backoff and respect for rate limit headers
2. **Configurability**: Make parameters configurable via CLI arguments and environment variables
3. **Testability**: Improve modularity to facilitate unit testing
4. **Observability**: Add better logging, metrics, and health checks
5. **Type precision**: Replace generic `Any` types with more specific domain types

These improvements would transform the script from a nice demonstration into a robust, production-ready tool suitable for integration into larger systems or regular automated use.