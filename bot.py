import os
import time
import logging
from dotenv import load_dotenv
from binance.client import Client
from binance.enums import *
from binance.exceptions import BinanceAPIException

# Load .env
load_dotenv()
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

# Logging
logging.basicConfig(filename='bot.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class BasicBot:
    def __init__(self):
        self.client = Client(API_KEY, API_SECRET, testnet=True)
        self.client.FUTURES_URL = 'https://testnet.binancefuture.com/fapi'
        self.sync_time_offset()

    def sync_time_offset(self):
        try:
            server_time = self.client.futures_time()['serverTime']
            local_time = int(time.time() * 1000)
            self.time_offset = server_time - local_time
        except Exception as e:
            logging.error(f"Time sync failed: {e}")
            self.time_offset = 0

    def get_timestamp(self):
        return int(time.time() * 1000) + self.time_offset

    def place_order(self, symbol, side, order_type, quantity, price=None):
        try:
            if order_type == "MARKET":
                order = self.client.futures_create_order(
                    symbol=symbol,
                    side=side,
                    type=order_type,
                    quantity=quantity,
                    timestamp=self.get_timestamp()
                )
            elif order_type == "LIMIT":
                order = self.client.futures_create_order(
                    symbol=symbol,
                    side=side,
                    type=order_type,
                    timeInForce=TIME_IN_FORCE_GTC,
                    quantity=quantity,
                    price=price,
                    timestamp=self.get_timestamp()
                )
            else:
                raise ValueError("Unsupported order type")

            logging.info(f"Order successful: {order}")
            print("Order successful:", order)
        except BinanceAPIException as e:
            logging.error(f"Binance API error: {e}")
            print("Binance API error:", e)
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            print("Unexpected error:", e)

if __name__ == "__main__":
    bot = BasicBot()
    print("Welcome to Binance Testnet Trading Bot")

    try:
        symbol = input("Enter symbol (e.g., BTCUSDT): ").upper()
        side = input("Enter side (BUY or SELL): ").upper()
        order_type = input("Enter order type (MARKET or LIMIT): ").upper()
        quantity = float(input("Enter quantity: "))

        price = None
        if order_type == "LIMIT":
            price = input("Enter price: ")

        bot.place_order(symbol, side, order_type, quantity, price)
    except Exception as e:
        logging.error(f"Input error: {e}")
        print("Invalid input.")
