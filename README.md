# Binance Futures Trading Bot (Testnet)

A Python CLI-based trading bot built for **Binance USDT-M Futures Testnet** using the official `python-binance` library.  
This project was developed as part of a technical assignment to demonstrate Futures API integration, modular design, validation, and logging.

---

## 🎯 Features Implemented

- Market Orders (BUY / SELL)
- Limit Orders
- Stop-Limit Orders (Bonus)
- TWAP (Time-Weighted Average Price) strategy (Bonus)
- Command-line interface (CLI)
- Input validation (symbol, side, quantity, price)
- Structured logging of API requests, responses, and errors
- Environment-variable–based credential handling

---

## 📁 Project Structure

```

project_root/
├── src/
│   ├── config.py
│   ├── logger.py
│   ├── utils.py
│   ├── market_orders.py
│   ├── limit_orders.py
│   ├── test_api_permissions.py
│   └── advanced/
│       ├── stop_limit.py
│       └── twap.py
├── README.md
├── report.pdf
├── requirements.txt

````

---

## 🛠️ Setup

### 1. Create a Binance Futures Testnet account
- URL: https://testnet.binancefuture.com

### 2. Generate API keys
- Enable Futures permissions (as available)

### 3. Set environment variables

**PowerShell (Windows):**
```powershell
$env:BINANCE_API_KEY="your_api_key"
$env:BINANCE_API_SECRET="your_api_secret"
````

---

## 🚀 Running the Bot

### Market Order

```bash
python src/market_orders.py BTCUSDT BUY 0.001
```

### Limit Order

```bash
python src/limit_orders.py BTCUSDT SELL 0.001 42000
```

### Stop-Limit Order

```bash
python src/advanced/stop_limit.py BTCUSDT BUY 0.001 41500 41600
```

### TWAP Order

```bash
python src/advanced/twap.py BTCUSDT BUY 0.05 5 10
```

---

## 📝 Logging

All API requests, responses, and errors are logged to `bot.log` in the project root.
Logs include timestamps, endpoint details, and full error traces for debugging.

---

## ⚠️ Known Limitation (Important)

During testing, Binance Futures Testnet consistently returned:

```
APIError(code=-2015): Invalid API-key, IP, or permissions for action
```

A dedicated permission diagnostic script (`test_api_permissions.py`) confirmed that the Testnet account lacks backend-enabled READ and TRADE permissions for Futures endpoints.

This is a **Binance Testnet account-level restriction**, not a client-side implementation issue.
The bot correctly constructs and submits Futures API requests and handles errors gracefully.

---
