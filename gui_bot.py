import os
import time
import tkinter as tk
from tkinter import ttk, messagebox, font
from dotenv import load_dotenv
from binance.client import Client
from binance.enums import *

# Load API keys
load_dotenv()
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

# Time sync
def get_timestamp_offset(client):
    server_time = client.futures_time()['serverTime']
    local_time = int(time.time() * 1000)
    return server_time - local_time

# Place order function
def place_order():
    symbol = symbol_entry.get().upper()
    side = side_combo.get().upper()
    order_type = type_combo.get().upper()
    quantity = float(qty_entry.get())
    price = price_entry.get()

    try:
        client = Client(API_KEY, API_SECRET, testnet=True)
        client.FUTURES_URL = 'https://testnet.binancefuture.com/fapi'
        offset = get_timestamp_offset(client)
        timestamp = int(time.time() * 1000) + offset

        if order_type == "MARKET":
            order = client.futures_create_order(
                symbol=symbol,
                side=side,
                type=order_type,
                quantity=quantity,
                timestamp=timestamp
            )
        elif order_type == "LIMIT":
            order = client.futures_create_order(
                symbol=symbol,
                side=side,
                type=order_type,
                timeInForce=TIME_IN_FORCE_GTC,
                quantity=quantity,
                price=price,
                timestamp=timestamp
            )
        else:
            raise ValueError("Unsupported order type")

        messagebox.showinfo("Success", f"Order Placed!\nStatus: {order['status']}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# GUI setup
root = tk.Tk()
root.title(" Binance Futures Trading Bot")
root.geometry("400x320")
root.configure(bg="#ecf0f1")

# Fonts
label_font = ("Helvetica", 10, "bold")
entry_font = ("Helvetica", 10)

# Labels & Inputs
def add_label_entry(text, row, entry_var=None):
    label = tk.Label(root, text=text, font=label_font, bg="#ecf0f1")
    label.grid(row=row, column=0, sticky="e", padx=10, pady=6)
    entry = tk.Entry(root, font=entry_font, width=20)
    entry.grid(row=row, column=1, padx=10)
    return entry

symbol_entry = add_label_entry("Symbol (e.g., BTCUSDT):", 0)
qty_entry = add_label_entry("Quantity:", 3)
price_entry = add_label_entry("Price (only for LIMIT):", 4)

# Side and Type dropdowns
tk.Label(root, text="Side:", font=label_font, bg="#ecf0f1").grid(row=1, column=0, sticky="e", padx=10, pady=6)
side_combo = ttk.Combobox(root, values=["BUY", "SELL"], font=entry_font)
side_combo.grid(row=1, column=1, padx=10)

tk.Label(root, text="Order Type:", font=label_font, bg="#ecf0f1").grid(row=2, column=0, sticky="e", padx=10, pady=6)
type_combo = ttk.Combobox(root, values=["MARKET", "LIMIT"], font=entry_font)
type_combo.grid(row=2, column=1, padx=10)

# Submit Button
place_button = tk.Button(root, text="Place Order", font=("Helvetica", 11, "bold"), bg="#3498db", fg="white", command=place_order)
place_button.grid(row=5, column=0, columnspan=2, pady=20)

root.mainloop()
