#!/usr/bin/env python3
"""
Bitcoin Price Monitor - Monitors BTC price alerts for >2% movement
"""
import requests
from datetime import datetime, timedelta
import time
import json

# Current monitoring parameters
CURRENT_PRICE = 65706.0  # $65,706 as of April 4, 2026
THRESHOLD_PERCENT = 0.02  # 2%
THRESHOLD_UP = CURRENT_PRICE * (1 + THRESHOLD_PERCENT)  # $67,020.12
THRESHOLD_DOWN = CURRENT_PRICE * (1 - THRESHOLD_PERCENT)  # $64,391.88

PRICE_URL = "https://api.coincap.io/v2/assets/bitcoin"  # Free, reliable API
ALERT_LOG = "/home/wherd/.openclaw/workspace/calendar/alerts/bitcoin_movements.json"

def fetch_bitcoin_price():
    """Fetch current Bitcoin price"""
    try:
        response = requests.get(PRICE_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        return float(data['data']['priceUsd'])
    except Exception as e:
        print(f"Error fetching price: {e}")
        return None

def check_and_alert(current_price):
    """Check if price has moved beyond thresholds"""
    movement_percent = ((current_price - CURRENT_PRICE) / CURRENT_PRICE) * 100
    
    alert = False
    status = ""
    
    if abs(movement_percent) > 2:
        alert = True
        if movement_percent > 0:
            status = "UP"
        else:
            status = "DOWN"
        
        print(f"⚠️  PRICE ALERT! Bitcoin has {movement_percent:+.2f}% from baseline")
        print(f"   Current: ${current_price:,.2f} | Up/Down: {status}")
        print(f"   Threshold: {THRESHOLD_UP:,.2f} / {THRESHOLD_DOWN:,.2f}")
        
        return True, movement_percent, status
    return False, 0, "STABLE"

def save_movement_alert(capture_time, current_price, movement_pct, direction, movement_reason):
    """Log price movement alert"""
    import os
    os.makedirs(os.path.dirname(ALERT_LOG), exist_ok=True)
    
    log_entry = {
        "timestamp": capture_time,
        "price": current_price,
        "movement_pct": movement_pct,
        "direction": direction,
        "movement_reason": movement_reason
    }
    
    try:
        with open(ALERT_LOG, 'a') as f:
            f.write(json.dumps(log_entry) + "\n")
        print(f"✓ Alert logged to: {ALERT_LOG}")
    except Exception as e:
        print(f"Error logging alert: {e}")

def generate_price_report():
    """Generate full price report"""
    current_price = fetch_bitcoin_price()
    
    if current_price is None:
        print("Cannot fetch price from API")
        return
    
    movement_pct = ((current_price - CURRENT_PRICE) / CURRENT_PRICE) * 100
    status = "STABLE" if abs(movement_pct) <= 2 else "ALERT"
    
    report = f"""
📊 BITCOIN PRICE REPORT
─────────────────────────────
📅 Date: {datetime.now().strftime('%-m/%d/%Y %H:%M')} (PDT)
💰 Current Price: ${current_price:,.2f}
📉 24h Change: {movement_pct:+.2f}% (from baseline ${CURRENT_PRICE:,.2f})

🎯 Threshold Status: {status}
   ── Target Alert (>2%):
   • UP Limit: ${THRESHOLD_UP:,.2f}
   • DOWN Limit: ${THRESHOLD_DOWN:,.2f}

📈 Market Analysis:
   • If {current_price:,.2f} moves beyond ±2%, you'll get an alert
   • Historical volatility: High
   • 2-Day pattern: Monitor closely

✅ {status}
"""
    return report, movement_pct, status

def main():
    """Main monitoring loop"""
    print("=== Bitcoin Price Monitor Started ===")
    print(f"Monitoring Bitcoin at ${CURRENT_PRICE:,.2f}")
    print(f"Alert threshold: ±{THRESHOLD_PERCENT*100}%")
    print(f"Target range: ${THRESHOLD_DOWN:,.2f} to ${THRESHOLD_UP:,.2f}")
    print()
    
    print("Starting monitoring...")
    print("Press Ctrl+C to stop monitoring")
    print()
    
    try:
        while True:
            current_price = fetch_bitcoin_price()
            if current_price:
                alert, movement_pct, status = check_and_alert(current_price)
                
                if alert:
                    Generate_price_report(current_price, movement_pct)
                    # Save alert to file
                    movement_reason = "Volatility spike detected"
                    save_movement_alert(
                        datetime.now().isoformat(),
                        current_price,
                        movement_pct,
                        status,
                        movement_reason
                    )
                
                print(f"Current price: ${current_price:,.2f} | Status: {status}")
                
                # Wait before next check
                print("Waiting 30 minutes for next check...")
                time.sleep(1800)  # 30 minutes
                
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()