import tkinter as tk
from tkinter import ttk, messagebox
import requests
import datetime
import threading
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation

API_KEY = os.getenv('API_KEY', 'YOURAPIKEY')
API_SECRET = os.getenv('API_SECRET', 'YOURSECRETAPI')
def log_price(symbol, price):
    """
    Logs the fetched price along with the timestamp to a file.
    """
    with open("price_log.txt", "a") as log_file:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"{timestamp} - {symbol}: {price}\n")

def fetch_price():
    symbol = symbol_entry.get().upper()
    if not symbol.endswith("USD"):
        symbol += "USD"
        symbol_entry.delete(0, tk.END)  # Clear the entry widget
        symbol_entry.insert(0, symbol)  # Insert the modified symbol back into the widget
    if symbol:
        price = get_crypto_price(symbol)
        if price == "Failed to fetch data":
            messagebox.showerror("Error", "Failed to fetch data. Please check the cryptocurrency symbol and try again.")
        else:
            price_var.set(f"Current Price: {price}")
            log_price(symbol, price)  # Log the fetched price
    else:
        messagebox.showinfo("Info", "Please enter a cryptocurrency symbol.")

def get_crypto_price(symbol):
    url = f"https://api.gemini.com/v1/pubticker/{symbol}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        price = data.get('last', 'No price available')
        return float(price) if price != 'No price available' else price
    else:
        return "Failed to fetch data"
    
def update():
    global prices, times
    price = get_crypto_price("BTCUSD")  # Example symbol
    prices.append(price)
    times.append(datetime.datetime.now())
    # Keep last 60 seconds of data
    if len(times) > 60:
        prices = prices[-60:]
        times = times[-60:]
    # Update plot
    ax.clear()
    ax.plot(times, prices)
    ax.xaxis_date()
    figure.autofmt_xdate()
    canvas.draw()
    # Update price display
    price_var.set(f"Current Price: {price}")
    # Schedule next update
    root.after(1000, update)

root = tk.Tk()
root.title("Crypto Price Checker")

prices = []
times = []

price_var = tk.StringVar()
price_label = ttk.Label(root, textvariable=price_var)
price_label.pack(padx=5, pady=5)

frame = ttk.Frame(root, padding="12")
frame.pack(padx=5, pady=5, fill=tk.X, expand=True)

figure, ax = plt.subplots()
canvas = FigureCanvasTkAgg(figure, master=root)
widget = canvas.get_tk_widget()
widget.pack()


price_var = tk.StringVar()

frame = ttk.Frame(root, padding="12")
frame.pack(padx=5, pady=5, fill=tk.X, expand=True)

symbol_label = ttk.Label(frame, text="Enter Cryptocurrency Symbol (e.g., BTCUSD):")
symbol_label.pack(padx=5, pady=5)

symbol_entry = ttk.Entry(frame, width=50)
symbol_entry.pack(padx=5, pady=5)
symbol_entry.focus()
symbol_entry.bind('<Return>', lambda event=None: fetch_price())

fetch_button = ttk.Button(frame, text="Fetch Price", command=fetch_price)
fetch_button.pack(padx=5, pady=5)

price_label = ttk.Label(frame, textvariable=price_var)
price_label.pack(padx=5, pady=5)

# Setup Matplotlib Figure and Axes
fig, ax = plt.subplots()
line, = ax.plot([], [], lw=2)

# Initialize the graph data source
graph_data = {
    "x_data": [],
    "y_data": []
}

def init():
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    return line,
fig, ax = plt.subplots()
x_data, y_data = [], []  # Step 3: Initialize lists for data

def update_graph(frame):
    # Fetch the latest price
    symbol = "BTCUSD"  # Example symbol, modify as needed
    price = get_crypto_price(symbol)
    timestamp = datetime.datetime.now()
    
    # Append new data to lists
    x_data.append(timestamp)
    y_data.append(price)
    
    # Clear the axes and plot the new data
    ax.clear()
    ax.plot(x_data, y_data)
    
    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('Real-Time Cryptocurrency Price')
    plt.ylabel('Price (USD)')

canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack()
ani = FuncAnimation(fig, update_graph, interval=1000) 
# plt.show()  # Commented out to prevent extra windows from opening
update()  # Initial call to start the updates

root.mainloop()
