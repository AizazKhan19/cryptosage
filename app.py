import google.genai.types as genai_types
import streamlit as st
import requests
from technical_indicators import calulate_rsi
from technical_indicators import calculate_macd
import joblib
import numpy as np
from agents.technical_agent_indicator import TechnicalAnalysisAgent
from google.adk.runners import InMemoryRunner
import asyncio
import dotenv

dotenv.load_dotenv()




# load the trained model---------------------------------------------------------------

model = joblib.load('linear_regression_model.plk')

st.title("CryptoSage")

# sidebar-------------------------------------------------------------------------------

st.sidebar.title("CryptoCurrencies")


# Dropdown menu for selecting cryptocurrency------------------------------------------------

cryptocurrencies = ["---Select Coin---", "BTC", "ETH"]
selected_crypto = st.sidebar.selectbox( 'Choose a cryptocurrency', cryptocurrencies)

# Mapping selected cryptocurrency to Binance symbol------------------------------------------------

crypto_map = {
    "BTC": "BTCUSDT",
    "ETH": "ETHUSDT"
}


    

# TImeframe selection---------------------------------------------------------------------

st.sidebar.title("Timeframe")
timeframes = ["---Select Timeframe---", "1m", "5m", "15m", "30m", "1h", "4h", "1d"]
selected_timeframe =  st.sidebar.selectbox('Choose a timeframe', timeframes)


# Analyze button--------------------------------------------------------------------------

clicked = st.sidebar.button('Analyze')

if clicked:
    # validtion for cryptocurrency and timeframe selection

    if selected_crypto == "---Select Coin---" or selected_timeframe == "---Select Timeframe---":
        st.sidebar.error("⚠️ Please select both cryptocurrency and timeframe properly!")
        st.stop()

    symbol = crypto_map[selected_crypto]
    
    with st.spinner("Analyzing..."):
        st.write(f"Analyzing {symbol} on {selected_timeframe} timeframe...")

        #  Fetching price---------------------------------------------------------------

        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
        response = requests.get(url)
        data = response.json()
        price = float(data['price'])
        price = round(price, 2)
        
        st.subheader(f"Current Price of {selected_crypto}")
        st.success(f"${price}")
        
        # Chart code--------------------------------------------------------------------

        price_chart_url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={selected_timeframe}&limit=50"
        price_chart_response = requests.get(price_chart_url)
        kline_data = price_chart_response.json()
        
        close_prices = []
        for row in kline_data:
            close_prices.append(float(row[4]))
        
        st.subheader(f"Price Chart of {selected_crypto} on {selected_timeframe} timeframe")
        st.line_chart(close_prices)
        
        # RSI code-----------------------------------------------------------------------

        current_rsi = calulate_rsi(close_prices)
        st.subheader("📊 Technical Indicators")
        st.metric("RSI (14-period)", f"{current_rsi:.2f}")
        
        if current_rsi > 70:
            st.warning("⚠️ Overbought - Potential SELL signal")
        elif current_rsi < 30:
            st.success("✅ Oversold - Potential BUY signal")
        else:
            st.info("➡️ Neutral - No strong signal")

        # MACD code----------------------------------------------------------------------

        macd_value, signal_value, macd_decision = calculate_macd(close_prices)

        # using columns for side by side display
        col1, col2 = st.columns(2)
        with col1:
            st.metric("MACD Line", f"{macd_value:.2f}")
        with col2:
            st.metric("Signal Line", f"{signal_value:.2f}")

        # show decision with color coding
        if "BUY" in macd_decision:
            st.success(f"📈 {macd_decision}")
        elif "SELL" in macd_decision:
            st.warning(f"📉 {macd_decision}")
        else:
            st.info(f"➡️ {macd_decision}")

        # Price Prediction code-------------------------------------------------------
        st.subheader("🔮 Price Prediction")
        st.info("Predicting the next closing price based on the last 5 closing prices using a Linear Regression model.")    
        
        # normalizing the close prices for prediction
        close_prices = np.array(close_prices)
        normalized_close_prices = (close_prices - min(close_prices)) / (max(close_prices) - min(close_prices))

        # picking last 5 close prices from the normalized close prices
        last_five_values = normalized_close_prices[-5:]

        # reshaping the last five normalize values
        last_five_reshaped_values = last_five_values.reshape(1, -1)

        # predicting the price

        predicted_price = model.predict(last_five_reshaped_values)

        # denormalizing the predicted price
        denormalized_predicted_price = predicted_price * (max(close_prices) - min(close_prices)) + min(close_prices)

        st.metric("Predicted Next Closing Price", f"${denormalized_predicted_price[0]:.2f}")

        # calling techincal agent-------------------------------------------------------------------
        st.subheader("🤖 Technical Analysis Agent")

        # creating runner------------------------------------------------------------------------------
        my_agent = TechnicalAnalysisAgent()
        runner = InMemoryRunner(agent = my_agent)

        input_string = f"RSI = {current_rsi}, MACD = {macd_value}, Signal = {signal_value}"

        response = asyncio.run(runner.run_debug(input_string))
        response_text = response[0].content.parts[0].text
        st.write("Technical Analysis Agent's Decision:")
        st.write(response_text)





