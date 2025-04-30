This is a simple Stock Ticker I created based on the code used for my Cypto Ticker, this is coded to run a Adafruit Matrix Portal M4

You need to create your settings.toml file for the code to run correctly, your wifi info and API key is pulled from here. 

Create a Finhub account to get your personal API key - https://finnhub.io/  

Your settings.toml should look something like this 

  
    # Comments are supported
    CIRCUITPY_WIFI_SSID ="ENTER YOUR NETWORK NAME HERE"
    CIRCUITPY_WIFI_PASSWORD ="ENTER YOUR NETWORK PASSWORD HERE"
    CIRCUITPY_WEB_API_PORT = 80
    CIRCUITPY_WEB_API_PASSWORD ="passw0rd"
    FINNHUB_API_KEY="ENTER YOUR KEY HERE"
