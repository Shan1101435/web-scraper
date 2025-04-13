import requests
import csv

# OpenWeatherMap API 金鑰
API_KEY = "54680892a7c824c03ee88d10541b92ad"

# 要查詢的城市名稱
CITY = "Taipei"

# API 請求的網址，包含城市名稱、API 金鑰、單位為攝氏 (metric)、語言為繁體中文
URL = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric&lang=zh_tw"

# 函式：向 API 發送請求並取得天氣資料
def fetch_weather():
    response = requests.get(URL)
    data = response.json()
    
    if data.get("cod") != 200:
        print(f"⚠️ API 錯誤: {data.get('message')}")
        return None

    weather_info = {
        "城市": data["name"],
        "溫度(°C)": data["main"]["temp"],
        "濕度(%)": data["main"]["humidity"],
        "天氣狀況": data["weather"][0]["description"],
    }
    return weather_info

# 函式：將天氣資料寫入 CSV 檔案
def save_to_csv(data, filename="api/api.csv"):
    if data is None:
        print("❌ 無法獲取天氣資訊")
        return

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=data.keys())
        writer.writeheader()
        writer.writerow(data)

    print(f"✅ 天氣資訊已儲存到 {filename}")

# 主程式
if __name__ == "__main__":
    weather_data = fetch_weather()
    save_to_csv(weather_data)
