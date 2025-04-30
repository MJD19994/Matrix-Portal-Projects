I have create a Stock Ticker that displays current price, percentage changed (reflects red when negative and green when positive), a historical graph.

It is intended to be used with a 64by64 Matrix

You need to create 2 files for the code to run correctly

1st) settings.toml which to contains your wifi netowrk info

    CIRCUITPY_WIFI_SSID = "your_wifi_ssid"
    CIRCUITPY_WIFI_PASSWORD = "your_wifi_password"
    ADAFRUIT_AIO_USERNAME = "your_aio_username"
    ADAFRUIT_AIO_KEY = "your_aio_key"

2nd) coin_config.txt which tells the software which coins you wish to track and display, there is an example of this provided along with the main code
    
    BTC, bitcoin
    ETH, ethereum
    XRP, ripple
    DOGE, dogecoin


I have uploaded many versions as I have add functions and removed issues, the current stable version is CyrptoTickerV1.0

MatrixPortalS3/CircuitPython/CyrptoTicker/CryptoTicker_AlphaV1.0
