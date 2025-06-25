# Binance Futures Testnet Trading Bot

A Python-based trading bot that connects to the **Binance USDT-M Futures Testnet**, allowing users to place `MARKET` and `LIMIT` orders using either a **Command-Line Interface (CLI)** or a **Graphical User Interface (GUI)** built with Tkinter.

---

##  Features

-  Loads API keys from `.env`
-  Supports Market and Limit orders
-  Time sync to prevent timestamp errors
-  Logs all activity to `bot.log`
-  Two modes:
  - `bot.py` – Command-Line version
  - `gui_bot.py` – GUI version with styled interface

---

##  Requirements

- Python 3.9+
- `python-binance==1.0.16`
- `aiohttp==3.8.1`
- `python-dotenv`
- Tkinter (comes with Python on most systems)

Install dependencies:
```bash
pip install -r requirements.txt
