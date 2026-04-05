#!/usr/bin/env python3
"""
Bitcoin Price Tracker

Fetches Bitcoin price history from CoinGecko API and calculates
a 7-day simple moving average (SMA).
"""

from __future__ import annotations

import logging
import sys
from datetime import datetime, timedelta, timezone
from typing import Any

import requests

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

COINGECKO_API_URL = "https://api.coingecko.com/api/v3"


def fetch_btc_price_history(days: int = 30) -> list[dict[str, Any]]:
    """
    Fetch Bitcoin price history from CoinGecko.

    Args:
        days: Number of historical days to fetch (default 30 to have enough data for SMA).

    Returns:
        A list of dicts with 'date' and 'price_usd' keys, sorted by date ascending.

    Raises:
        requests.exceptions.RequestException: If the API request fails.
        ValueError: If the response data is malformed.
    """
    url = f"{COINGECKO_API_URL}/coins/bitcoin/market_chart"
    params = {
        "vs_currency": "usd",
        "days": days,
        "interval": "daily",
    }

    logger.info(f"Fetching Bitcoin price history for the last {days} days...")

    try:
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
    except requests.exceptions.HTTPError as exc:
        if response.status_code == 429:
            logger.error("Rate limited by CoinGecko API. Please wait and try again.")
        else:
            logger.error(f"HTTP error: {response.status_code} - {response.text}")
        raise
    except requests.exceptions.ConnectionError:
        logger.error("Failed to connect to CoinGecko API. Check your internet connection.")
        raise
    except requests.exceptions.Timeout:
        logger.error("Request to CoinGecko API timed out.")
        raise

    data = response.json()

    if "prices" not in data or not isinstance(data["prices"], list):
        raise ValueError("Unexpected API response: 'prices' key missing or not a list.")

    price_data: list[dict[str, Any]] = []
    for entry in data["prices"]:
        if len(entry) < 2:
            continue
        timestamp_ms = entry[0]
        price_usd = entry[1]
        date = datetime.fromtimestamp(timestamp_ms / 1000, tz=timezone.utc).date()
        price_data.append({"date": date, "price_usd": price_usd})

    price_data.sort(key=lambda x: x["date"])
    logger.info(f"Successfully fetched {len(price_data)} price records.")
    return price_data


def calculate_sma(price_data: list[dict[str, Any]], window: int = 7) -> list[dict[str, Any]]:
    """
    Calculate the Simple Moving Average (SMA) over a given window.

    Args:
        price_data: List of dicts with 'date' and 'price_usd' keys, sorted by date.
        window: The SMA window size in days (default 7).

    Returns:
        A list of dicts with 'date', 'price_usd', and 'sma_7d' keys.
        SMA values will be None where insufficient data exists.

    Raises:
        ValueError: If window is less than 1 or price_data is empty.
    """
    if window < 1:
        raise ValueError("Window size must be at least 1.")
    if not price_data:
        raise ValueError("Price data cannot be empty.")

    result: list[dict[str, Any]] = []
    prices: list[float] = []

    for i, entry in enumerate(price_data):
        prices.append(entry["price_usd"])
        if len(prices) >= window:
            sma = sum(prices[-window:]) / window
        else:
            sma = None
        result.append({
            "date": entry["date"],
            "price_usd": entry["price_usd"],
            "sma_7d": sma,
        })

    return result


def display_results(results: list[dict[str, Any]]) -> None:
    """
    Display the price and SMA data in a formatted table.

    Args:
        results: List of dicts with 'date', 'price_usd', and 'sma_7d' keys.
    """
    if not results:
        logger.warning("No results to display.")
        return

    header = f"{'Date':<12} {'Price (USD)':>12} {'7-Day SMA':>12}"
    separator = "-" * len(header)
    print(f"\n{header}")
    print(separator)

    for entry in results:
        date_str = entry["date"].isoformat()
        price_str = f"${entry['price_usd']:,.2f}"
        sma_str = f"${entry['sma_7d']:,.2f}" if entry["sma_7d"] is not None else "N/A"
        print(f"{date_str:<12} {price_str:>12} {sma_str:>12}")

    print(separator)
    latest = results[-1]
    print(f"\nLatest Bitcoin Price: ${latest['price_usd']:,.2f}")
    if latest["sma_7d"] is not None:
        print(f"7-Day Moving Average: ${latest['sma_7d']:,.2f}")
    else:
        print("7-Day Moving Average: N/A (insufficient data)")


def main() -> None:
    """Main entry point for the Bitcoin price tracker."""
    try:
        price_data = fetch_btc_price_history(days=30)
        results = calculate_sma(price_data, window=7)
        display_results(results)
    except requests.exceptions.RequestException:
        logger.error("Failed to fetch price data. Exiting.")
        sys.exit(1)
    except ValueError as exc:
        logger.error(f"Data error: {exc}")
        sys.exit(1)
    except Exception as exc:
        logger.exception(f"Unexpected error: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
