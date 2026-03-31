import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

from config import API_KEY
from utils import get_weather_emoji, get_aqi_label, save_history

st.set_page_config(page_title="Weather Dashboard", page_icon="🌦️")

st.title("🌦️ Smart Weather Dashboard")
st.write("Weather + Forecast + AQI + History 📊")

city = st.text_input("Enter city name")

if st.button("Get Weather"):
    if not city:
        st.warning("⚠️ Please enter a city name")
        st.stop()

    # ---------------- CURRENT WEATHER ----------------
    weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    res = requests.get(weather_url)

    if res.status_code != 200:
        st.error("❌ City not found")
        st.stop()

    data = res.json()

    temp = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]
    humidity = data["main"]["humidity"]
    pressure = data["main"]["pressure"]
    wind = data["wind"]["speed"]
    condition = data["weather"][0]["description"]

    lat = data["coord"]["lat"]
    lon = data["coord"]["lon"]

    emoji = get_weather_emoji(condition)

    st.success(f"{emoji} Weather in {city}")

    col1, col2, col3 = st.columns(3)
    col1.metric("🌡️ Temp", temp)
    col2.metric("🤔 Feels Like", feels_like)
    col3.metric("💧 Humidity", humidity)

    st.write(f"☁️ Condition: {condition}")
    st.write(f"🌬️ Wind: {wind} m/s")
    st.write(f"ضغط Pressure: {pressure} hPa")

    # ---------------- AQI ----------------
    aqi_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
    aqi_res = requests.get(aqi_url)

    if aqi_res.status_code == 200:
        aqi_data = aqi_res.json()
        aqi = aqi_data["list"][0]["main"]["aqi"]

        st.subheader("🌫️ Air Quality Index")
        st.metric("AQI Level", aqi)
        st.write(get_aqi_label(aqi))
    else:
        st.warning("⚠️ AQI data unavailable")

    # ---------------- FORECAST ----------------
    forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
    res = requests.get(forecast_url)

    forecast_list = []
    shown_dates = set()

    if res.status_code == 200:
        forecast_data = res.json()

        for item in forecast_data["list"]:
            date = item["dt_txt"].split(" ")[0]

            if date not in shown_dates:
                shown_dates.add(date)

                forecast_list.append({
                    "Date": date,
                    "Temp (°C)": item["main"]["temp"],
                    "Condition": item["weather"][0]["description"],
                    "Emoji": get_weather_emoji(item["weather"][0]["description"])
                })

            if len(forecast_list) == 5:
                break

        df = pd.DataFrame(forecast_list)

        st.subheader("📅 5-Day Forecast")
        st.dataframe(df)

        # Chart
        st.subheader("📈 Temperature Trend")
        plt.figure()
        plt.plot(df["Date"], df["Temp (°C)"])
        plt.xlabel("Date")
        plt.ylabel("Temperature (°C)")
        plt.title("5-Day Trend")

        st.pyplot(plt)

    # ---------------- SAVE HISTORY ----------------
    history_data = {
        "timestamp": datetime.now(),
        "city": city,
        "temperature": temp,
        "condition": condition,
        "humidity": humidity,
        "aqi": aqi if aqi_res.status_code == 200 else None
    }

    save_history(history_data)

    st.success("✅ Search saved to history")

# ---------------- VIEW HISTORY ----------------
if st.checkbox("📂 View Search History"):
    try:
        df = pd.read_csv("data/history.csv")
        st.dataframe(df)
    except:
        st.info("No history found yet.")