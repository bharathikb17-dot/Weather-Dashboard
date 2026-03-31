import pandas as pd
import os

# 🌈 Emoji logic
def get_weather_emoji(condition):
    condition = condition.lower()

    if "clear" in condition:
        return "☀️"
    elif "cloud" in condition:
        return "☁️"
    elif "rain" in condition:
        return "🌧️"
    elif "snow" in condition:
        return "❄️"
    elif "thunder" in condition:
        return "⛈️"
    elif "mist" in condition or "fog" in condition:
        return "🌫️"
    else:
        return "🌍"

# 🌫️ AQI Interpretation
def get_aqi_label(aqi):
    labels = {
        1: "Good 😊",
        2: "Fair 🙂",
        3: "Moderate 😐",
        4: "Poor 😷",
        5: "Very Poor 🤢"
    }
    return labels.get(aqi, "Unknown")

# 💾 Save to CSV
def save_history(data, file_path="data/history.csv"):
    os.makedirs("data", exist_ok=True)

    df = pd.DataFrame([data])

    if os.path.exists(file_path):
        df.to_csv(file_path, mode='a', header=False, index=False)
    else:
        df.to_csv(file_path, index=False)