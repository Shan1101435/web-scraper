import requests
import csv

API_KEY = "54680892a7c824c03ee88d10541b92ad"
CITY = "Taipei"
URL = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric&lang=zh_tw"

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

def save_to_csv(data, filename="weather.csv"):
    if data is None:
        print("❌ 無法獲取天氣資訊")
        return
    
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=data.keys())
        writer.writeheader()
        writer.writerow(data)
    
    print(f"✅ 天氣資訊已儲存到 {filename}")

if __name__ == "__main__":
    weather_data = fetch_weather()
    save_to_csv(weather_data)