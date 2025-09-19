import tkinter as tk
import requests
import geocoder
from PIL import Image, ImageTk

# Переводим код погоды в иконку OpenWeatherMap
wmo_to_icon = {
    0: "01d", 1: "01d", 2: "02d", 3: "03d", 4: "04d",
    45: "50d", 48: "50d", 61: "10d", 71: "13d", 73: "13d",
    75: "13d", 77: "13d", 80: "09d", 81: "09d", 82: "09d",
    85: "13d", 86: "13d", 95: "11d", 96: "11d", 99: "11d"
}

# Переводим код погоды в чешские названия
wmo_to_weather = {
    0: "Jasná obloha", 1: "Jasná obloha", 2: "Částečně oblačno",
    3: "Rozptýlená oblačnost", 4: "Rozptýlená oblačnost",
    45: "Mlha", 48: "Mlha", 61: "Déšť", 71: "Sníh",
    73: "Sníh", 75: "Sníh", 77: "Sníh", 80: "Přeháňky",
    81: "Přeháňky", 82: "Přeháňky", 85: "Sníh", 86: "Sníh",
    95: "Bouřka", 96: "Bouřka", 99: "Bouřka"
}

# Получаем текущее местоположение по IP
g = geocoder.ip('me')

latitude = g.latlng[0]
longitude = g.latlng[1]
city = g.city if g.city else "Neznámé město"

# Функция для получения иконки погоды
def get_weather_icon(wmo_code):
    icon_code = wmo_to_icon.get(wmo_code, "01d")
    icon_url = f"http://openweathermap.org/img/w/{icon_code}.png"
    icon_response = requests.get(icon_url, stream=True)
    if icon_response.status_code == 200:
        icon_image = Image.open(icon_response.raw)
        icon_photo = ImageTk.PhotoImage(icon_image)
        return icon_photo
    else:
        return None

# Функция получения прогноза
def get_weather():
    URL = f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=weathercode,temperature_2m_max,temperature_2m_min&timezone=CET'
    response = requests.get(URL)
    data = response.json()
    
    for widget in window.winfo_children():
        if isinstance(widget, tk.Label) and widget not in [city_label, search_button]:
            widget.destroy()
    
    for idx, date in enumerate(data['daily']['time']):
        min_temp = data['daily']['temperature_2m_min'][idx]
        max_temp = data['daily']['temperature_2m_max'][idx]
        wmo_code = data['daily']['weathercode'][idx]
        weather_text = wmo_to_weather.get(wmo_code, "Jasná obloha")
        weather_icon = get_weather_icon(wmo_code)
        
        daily_info = f"Datum: {date}\nPočasí: {weather_text}\nMin. teplota: {min_temp}°C\nMax. teplota: {max_temp}°C"
        
        if weather_icon:
            icon_label = tk.Label(window, image=weather_icon, bg="#3498db")
            icon_label.image = weather_icon
            icon_label.grid(row=idx+2, column=0, padx=10, pady=5, sticky="w")
        
        label = tk.Label(window, text=daily_info, font=('Helvetica', 12), bg="#3498db", fg="white", wraplength=300, justify="left")
        label.grid(row=idx+2, column=1, padx=10, pady=5, sticky="w")

# Инициализация окна
window = tk.Tk()
window.title("Aplikace Počasí")
window.geometry("450x900")
window.configure(bg="#3498db")

# Заголовок с городом
city_label = tk.Label(window, text=f"Město: {city}", font=('Helvetica', 14, 'bold'), bg="#3498db", fg="white")
city_label.grid(row=0, column=0, columnspan=2, pady=10, padx=10)

# Кнопка запроса погоды
search_button = tk.Button(window, text="Získat počasí", command=get_weather, bg="#2ecc71", fg="white", relief="flat")
search_button.grid(row=1, column=0, columnspan=2, pady=10, padx=10)

window.mainloop()
