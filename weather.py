import tkinter as tk
from tkinter import messagebox
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from datetime import datetime
from dotenv import load_dotenv
import requests
import pytz
import os


root = tk.Tk()
root.title("Weather App")
root.geometry("900x500+300+200")
root.resizable(False,False)

def get_weather():
    try:
        # Location
        city = textfield.get()
        geolocator = Nominatim(user_agent="geopiExercises")
        location = geolocator.geocode(city, language='en', timeout=10)
        lat = location.latitude
        lng = location.longitude
        obj = TimezoneFinder()
        result = obj.timezone_at(lng=lng, lat=lat)

        location_data = geolocator.reverse("{0}, {1}".format(lat,lng), language='en', timeout=10)
        address = location_data.raw['address']
        country = address.get('country', '')
        city_label.config(text="{0}, {1}".format(country,city))

        # Time
        home = pytz.timezone(result)
        local_time = datetime.now(home)
        current_time = local_time.strftime("%I:%M %p")
        clock.config(text=current_time)
        time_label.config(text="LOCAL TIME")

        # Weather
        load_dotenv()
        api_key = os.getenv('OPENWEATHERMAP_API_KEY')
        api = "https://api.openweathermap.org/data/2.5/weather?lat={0}&lon={1}&appid={2}".\
            format(lat, lng, api_key)
        json_data = requests.get(api).json()
        condition = json_data["weather"][0]["main"]
        description = json_data["weather"][0]["description"]
        temp = int(json_data["main"]["temp"] - 273.15)
        pressure = json_data["main"]["pressure"]
        humidity = json_data["main"]["humidity"]
        wind = json_data["wind"]["speed"]

        # Show
        temp_label.config(text="{0}°".format(temp))
        condition_label.config(text="{0} | FEELS LIKE {1}°".format(condition,temp))
        wind_label.config(text=wind)
        humidity_label.config(text=humidity)
        description_label.config(text=description)
        pressure_label.config(text=pressure)

        if condition == "Clear":
            logo_image.config(file="clear_logo.png")
        elif condition == "Clouds":
            logo_image.config(file="Cloudy_logo.png")
        elif condition == "Atmosphere":
            logo_image.config(file="Atmosphere_logo.png")
        elif condition == "Snow":
            logo_image.config(file="Snow_logo.png")
        elif condition == "Rain" or "Drizzle":
            logo_image.config(file="Rain_logo.png")
        elif condition == "Thunderstorm":
            logo_image.config(file="Thunderstorm_logo.png")

    except Exception as error:
        print(error)
        messagebox.showerror("Weather App", "Invalid Entry")


def on_enter(event):
    # Hover
    search_icon_button.config(image=search_icon2)

def on_leave(event):
    # Normal
    search_icon_button.config(image=search_icon)


# Search Box
search_image = tk.PhotoImage(file="Searchbox.png")
search_image_lable = tk.Label(root, image=search_image)
search_image_lable.pack(pady=20,side=tk.TOP)
textfield = tk.Entry(root, justify="center", width=17, font=("poppins",25,"bold"),
                     bg="#003049", fg="white", border=0)
textfield.place(x=280, y=40)

# Search Icon
search_icon = tk.PhotoImage(file="search_icon1.png")
search_icon2 = tk.PhotoImage(file="search_icon2.png")
search_icon_button = tk.Button(root,image=search_icon, border=0,
                               bg="#003049", cursor="hand2", command=get_weather, activebackground="#003049")
search_icon_button.place(x=591, y=34)

search_icon_button.bind("<Enter>", on_enter)
search_icon_button.bind("<Leave>", on_leave)


# logo
logo_image = tk.PhotoImage(file="Weatherlogo.png")
logo_label = tk.Label(root,image=logo_image)
logo_label.pack(side=tk.TOP)

# Bottom Box
frame_image = tk.PhotoImage(file="box.png")
frame_label = tk.Label(root,image=frame_image)
frame_label.pack(pady=10,side=tk.TOP)

# City Name
city_label = tk.Label(root, font=("arial", 25, "bold"), fg="#e355cd")
city_label.place(x=75, y=160)

# Time
time_label = tk.Label(root, font=("arial", 15, "bold"), fg="#4b4bcc")
time_label.place(x=75, y=220)

clock = tk.Label(root, font=("Helvetica", 15), fg="#4b4bcc")
clock.place(x=75, y=250)

# Labels
label1 = tk.Label(root, text="WIND", font=("Helvetica", 15, "bold"),
                  fg="#1f1f1f", bg="#a8dadc")
label1.place(x=120, y=405)

label2 = tk.Label(root, text="HUMIDITY", font=("Helvetica", 15, "bold"),
                  fg="#1f1f1f", bg="#a8dadc")
label2.place(x=280, y=405)

label3 = tk.Label(root, text="DESCRIPTION", font=("Helvetica", 15, "bold"),
                  fg="#1f1f1f", bg="#a8dadc")
label3.place(x=450, y=405)

label4 = tk.Label(root, text="PRESSURE", font=("Helvetica", 15, "bold"),
                  fg="#1f1f1f", bg="#a8dadc")
label4.place(x=670, y=405)

wind_label = tk.Label(root,text=" ", font=("arial", 15, "bold"),
                      fg="#4b4bcc", bg="#a8dadc")
wind_label.place(x=120, y=435)

humidity_label = tk.Label(root,text=" ", font=("arial", 15, "bold"),
                      fg="#4b4bcc", bg="#a8dadc")
humidity_label.place(x=280, y=435)

description_label = tk.Label(root,text=" ", font=("arial", 15, "bold"),
                      fg="#4b4bcc", bg="#a8dadc")
description_label.place(x=450, y=435)

pressure_label = tk.Label(root,text=" ", font=("arial", 15, "bold"),
                      fg="#4b4bcc", bg="#a8dadc")
pressure_label.place(x=670, y=435)

# ------------------------------------------------------------------------

temp_label = tk.Label(root, font=("arial", 40, "bold"),fg="#e355cd")
temp_label.place(x=690, y=160)

condition_label = tk.Label(root, font=("arial", 15, "bold"),fg="#4b4bcc")
condition_label.place(x=610, y=240)

root.mainloop()
