import streamlit as st
import requests

st.title("CryptoSage")

# sidebar-------------------------------------------------------------------------------

st.sidebar.title("CryptoCurrencies")


# Dropdown menu for selecting cryptocurrency------------------------------------------------

cryptocurrencies = ["BTC", "ETH"]
selected_crypto = st.sidebar.selectbox( 'Choose a cryptocurrency', cryptocurrencies)

# Mapping selected cryptocurrency to Binance symbol------------------------------------------------

crypto_map = {
    "BTC": "BTCUSDT",
    "ETH": "ETHUSDT"
}

symbol = crypto_map[selected_crypto]
    

# TImeframe selection---------------------------------------------------------------------

st.sidebar.title("Timeframe")
timeframes = ["1m", "5m", "15m", "30m", "1h", "4h", "1d"]
selected_timeframe =  st.sidebar.selectbox('Choose a timeframe', timeframes)


# Analyze button--------------------------------------------------------------------------

clicked = st.sidebar.button('Analyze')

if clicked:
    with st.spinner("Analyzing..."):
        st.write(f"Analyzing {symbol} on {selected_timeframe} timeframe...")

# Fetching price from binance API-----------------------------------------------------------------------

url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"

# sending request
response = requests.get(url)

# print the data
# st.write(response.json())

#  extracting price from  response. for that first we need to store json data into varibale.

data = response.json()

# converting price to float because it is in string format
price = float(data['price'])

# rounding off price to 2 decimal places
price = round(price, 2)

# displaying price
st.subheader(f"Current Price of {selected_crypto}")
st.success(f"${price}")


# showing price chart of selected cryptocurrency using binance API

price_chart_url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={selected_timeframe}&limit=50"

# sending request
price_chart_response = requests.get(price_chart_url)

# storing kline data into varibale
kline_data = price_chart_response.json()

# creating empty list
close_prices = []

for row in kline_data:
    close_prices.append(float(row[4]))

# displaying price chart
st.subheader(f"Price Chart of {selected_crypto} on {selected_timeframe} timeframe")
st.line_chart(close_prices)