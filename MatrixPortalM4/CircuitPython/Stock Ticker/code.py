import gc
import time
import board
import displayio
import terminalio
import busio
from digitalio import DigitalInOut
from os import getenv
from rtc import RTC
from adafruit_ntp import NTP
import adafruit_connection_manager
import adafruit_requests
from adafruit_esp32spi import adafruit_esp32spi
import rgbmatrix
import framebufferio
from adafruit_display_text import label

# ========= Global Configuration =========
STOCK_SYMBOLS = ["AAPL", "GOOGL", "AMZN"]  # List of stock symbols
FETCH_INTERVAL = 3600  # Fetch new data every hour (3600 seconds)
API_KEY = getenv("FINNHUB_API_KEY")  # Load Finnhub API key from settings.toml
if not API_KEY:
    raise RuntimeError("FINNHUB_API_KEY not found in settings.toml")
URL_TEMPLATE = "https://finnhub.io/api/v1/quote?symbol={}&token=" + API_KEY
latest_prices = {}  # Cache for stock prices
last_fetched_time = 0

# ========= Matrix Setup =========
displayio.release_displays()
matrix = rgbmatrix.RGBMatrix(
    width=64,
    height=64,
    bit_depth=4,
    rgb_pins=[
        board.MTX_R1, board.MTX_G1, board.MTX_B1,
        board.MTX_R2, board.MTX_G2, board.MTX_B2
    ],
    addr_pins=[
        board.MTX_ADDRA, board.MTX_ADDRB, board.MTX_ADDRC,
        board.MTX_ADDRD, board.MTX_ADDRE
    ],
    clock_pin=board.MTX_CLK,
    latch_pin=board.MTX_LAT,
    output_enable_pin=board.MTX_OE
)
display = framebufferio.FramebufferDisplay(matrix, auto_refresh=True)

# ========= Wi-Fi and ESP32 Setup =========
ssid = getenv("CIRCUITPY_WIFI_SSID")
password = getenv("CIRCUITPY_WIFI_PASSWORD")

# ESP32 pins for Matrix Portal M4
esp32_cs = DigitalInOut(board.ESP_CS)
esp32_ready = DigitalInOut(board.ESP_BUSY)
esp32_reset = DigitalInOut(board.ESP_RESET)

# SPI Initialization
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)

pool = adafruit_connection_manager.get_radio_socketpool(esp)
ssl_context = adafruit_connection_manager.get_radio_ssl_context(esp)
requests = adafruit_requests.Session(pool, ssl_context)

def connect_to_wifi():
    display_message(["Connecting"], [24])
    print("Connecting to WiFi...")
    while not esp.is_connected:
        try:
            esp.connect_AP(ssid, password)
        except OSError as e:
            print("Could not connect to WiFi, retrying: ", e)
            continue
    print("Connected to WiFi")
    print("My IP address is", esp.ipv4_address)
    display_message(["Connected", "IP:", str(esp.ipv4_address)], [8, 24, 40])
    time.sleep(5)

def display_message(messages, y_positions):
    display_group = displayio.Group()
    for index, message in enumerate(messages):
        message_label = label.Label(terminalio.FONT, text=message, color=0xFFFFFF, x=0, y=y_positions[index])
        display_group.append(message_label)
    display.root_group = display_group

def check_and_sync_time(pool):
    """
    Checks the device's internal time and synchronizes it with an NTP server if needed.
    """
    try:
        # Get the current time from the device's RTC
        rtc = RTC()
        current_time = rtc.datetime
        print(f"Current RTC time: {current_time}")

        # If the time is obviously incorrect (e.g., year < 2023), sync with NTP
        if current_time.tm_year < 2023:
            print("RTC time is incorrect. Synchronizing with NTP...")
            
            # Initialize the NTP client
            ntp = NTP(pool, server="time.google.com", tz_offset=0)
            
            # Fetch the current time
            rtc.datetime = ntp.datetime
            synced_time = rtc.datetime
            print(f"RTC time synchronized to: {synced_time}")
        else:
            print("RTC time is already correct. No need to sync.")
    except Exception as e:
        print(f"Error during time synchronization: {e}")

connect_to_wifi()
check_and_sync_time(pool)

# ========= Data Fetching =========
def fetch_stock_data(symbol):
    try:
        print(f"Fetching data for {symbol}...")
        response = requests.get(URL_TEMPLATE.format(symbol))
        data = response.json()
        if not data or "c" not in data:
            print(f"Error: Missing data for {symbol}")
            return None
        price = data["c"]  # Current price
        change = data["d"]  # Price change
        percent_change = data["dp"]  # Percent change
        return {"price": price, "change": change, "percent_change": percent_change}
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None

# ========= Display Update =========
def update_display(symbol, data):
    if not data:
        display_message(["Error", "fetching data"], [16, 32])
        return
    price = data["price"]
    change = data["change"]
    percent_change = data["percent_change"]
    # Adjusted color definitions for GRB/BGR ordering
    change_color = 0x00FF00 if change < 0 else 0x0000FF  # Green for negative, Blue for positive (adjusted for GRB/BGR)
    display_group = displayio.Group()
    symbol_label = label.Label(terminalio.FONT, text=symbol, color=0xFFFFFF, x=0, y=8)
    price_label = label.Label(terminalio.FONT, text=f"${price:.2f}", color=0xFFFFFF, x=0, y=24)
    change_label = label.Label(terminalio.FONT, text=f"{percent_change:+.2f}%", color=change_color, x=0, y=40)
    display_group.append(symbol_label)
    display_group.append(price_label)
    display_group.append(change_label)
    display.root_group = display_group

# ========= Main Loop =========
while True:
    try:
        gc.collect()
        current_time = time.monotonic()
        # Fetch new data if interval has passed or cache is empty
        if current_time - last_fetched_time >= FETCH_INTERVAL or not latest_prices:
            latest_prices = {sym: fetch_stock_data(sym) for sym in STOCK_SYMBOLS}
            last_fetched_time = current_time
        # Cycle through cached stock data
        for symbol in STOCK_SYMBOLS:
            update_display(symbol, latest_prices.get(symbol))
            time.sleep(10)  # Show each stock for 10 seconds
    except Exception as e:
        print(f"Error in main loop: {e}")
        display_message(["Error", "Restarting..."], [16, 32])
        time.sleep(5)
